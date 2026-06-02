import { render, screen, fireEvent, waitFor} from '@testing-library/react';
import AuthModal from '../app/components/AuthModal';
import { useAuth } from '../app/context/AuthContext';
import { authService } from '../app/services';
import toast from 'react-hot-toast';

// mock AuthContext
jest.mock('../app/context/AuthContext', () => ({
    useAuth: jest.fn()
}));

// mock authService
jest.mock('../app/services', () => ({
    authService: {
        login: jest.fn(),
        register: jest.fn()
    }
}));


// mock toast
jest.mock('react-hot-toast', () => ({
    success: jest.fn(),
    error: jest.fn()
}));

describe('AuthModal Component', () => {
    const mockLogin = jest.fn();
    const mockOnClose = jest.fn();

    beforeEach(() => {
        // reset all mocks before each test
        jest.clearAllMocks();

        (useAuth as jest.Mock).mockReturnValue({
            login: mockLogin
        });
    });

    it('returns null and does not render if isOpen is false', () => {
        const { container } = render(<AuthModal isOpen={false} onClose={mockOnClose} />);
        expect(container).toBeEmptyDOMElement();
    });

    it('renders the login form by default when open', () => {
        render(<AuthModal isOpen={true} onClose={mockOnClose} />);
        expect(screen.getByText('Welcome Back!')).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Sign In' })).toBeInTheDocument();
    });

    it('toggles to the sign up form when the toggle button is clicked', () => {
        render(<AuthModal isOpen={true} onClose={mockOnClose} />);
        
        // find the toggle button and click it
        const toggleButton = screen.getByText('Sign up');
        fireEvent.click(toggleButton);

        // verify the UI changes to the registration state
        expect(screen.getByText('Create an Account')).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Create Account' })).toBeInTheDocument();
    });

    it('successfully submits the login form, calls the API, and fires a toast', async () => {
        // setup fake API to return a fake token
        (authService.login as jest.Mock).mockResolvedValue({ access_token: 'fake-jwt-token' });

        render(<AuthModal isOpen={true} onClose={mockOnClose} />);

        // fill out the form
        const emailInput = screen.getByPlaceholderText('you@example.com');
        const passwordInput = screen.getByPlaceholderText('••••••••');

        fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
        fireEvent.change(passwordInput, { target: { value: 'password123' } });

        // submit the form
        const submitButton = screen.getByRole('button', { name: 'Sign In' });
        fireEvent.click(submitButton);

        // waitFor is required because our handleSubmit is async 
        await waitFor(() => {
            // verify API was called with correct data
            expect(authService.login).toHaveBeenCalledWith({
                email: 'test@example.com',
                password: 'password123'
            });

            // verify login function from context was called with the token
            expect(mockLogin).toHaveBeenCalledWith('fake-jwt-token');

            // verify modal tries to close
            expect(mockOnClose).toHaveBeenCalled();

            // verify success toast is shown
            expect(toast.success).toHaveBeenCalled();
        });
    });

});
