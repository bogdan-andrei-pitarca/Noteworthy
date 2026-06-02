import { render, screen, fireEvent } from '@testing-library/react';
import Navbar from '../app/components/Navbar';
import { useAuth } from '../app/context/AuthContext';

// mock the Next.js router and Link components
jest.mock('next/link', () => {
    return ({ children }: { children: React.ReactNode }) => {
        return <a>{children}</a>
    }
});

// mock AuthContext
jest.mock('../app/context/AuthContext', () => ({
    useAuth: jest.fn()
}));

describe('Navbar Component', () => {
    it('renders the Sign In button when the user is NOT authenticated', () => {
        (useAuth as jest.Mock).mockReturnValue({
            isAuthenticated: false,
            logout: jest.fn(),
            login: jest.fn()
        });

        render(<Navbar />);

        // verify UI state
        expect(screen.getByText('Noteworthy.')).toBeInTheDocument();
        expect(screen.getByText('Sign In')).toBeInTheDocument();

        // verify protected elements are hidden
        expect(screen.queryByText('Favorites')).not.toBeInTheDocument();
        expect(screen.queryByText('Logout')).not.toBeInTheDocument();

    });

    it('renders Favorites and Logout when the user IS authenticated', () => {
        // fake authenticated state
        (useAuth as jest.Mock).mockReturnValue({
            isAuthenticated: true,
            logout: jest.fn(),
            login: jest.fn()
        });

        render(<Navbar />);

        // verify UI state
        expect(screen.getByText('Favorites')).toBeInTheDocument();
        expect(screen.getByText('Logout')).toBeInTheDocument();

        // verify Sign In is hidden
        expect(screen.queryByText('Sign In')).not.toBeInTheDocument();
    });

    it('opens the AuthModal when Sign In is clicked', () => {
        (useAuth as jest.Mock).mockReturnValue({
            isAuthenticated: false,
            logout: jest.fn(),
            login: jest.fn()
        });

        render(<Navbar />);

        // find and click the button
        const signInButton = screen.getByText('Sign In');
        fireEvent.click(signInButton);

        // verify the modal appears (looking for the text inside AuthModal)
        expect(screen.getByText('Welcome Back!')).toBeInTheDocument();
    });
});