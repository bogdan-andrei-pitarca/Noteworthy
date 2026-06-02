import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ResultCard from '../app/components/ResultCard';
import { fragranceService } from '../app/services';
import { FragranceRecord } from '../app/types/FragranceTypes';

// mock fragranceService
jest.mock('../app/services', () => ({
    fragranceService: {
        generateDescription: jest.fn()
    }
}));

// dummy record for testing
const mockFragrance: FragranceRecord = {
    embedding_id: 101,
    perfume_name: 'Plume Blanche 1901',
    brand: 'lalique',
    gender: 'unisex',
    launch_year: 2020,
    rating_value: 4.13,
    rating_count: 132,
    url: 'https://example.com/perfume',
    main_accord_1: 'Almond',
    main_accord_2: 'Vanilla',
    main_accord_3: 'none', // should be skipped by the filter
    main_accord_4: 'none',
    main_accord_5: 'none',
    all_notes: "['almond', 'vanilla', 'musk']",
    similarity_percent: 85.5
};

describe('ResultCard Component', () => {
    beforeEach(() => {
        // reset mocks before each test
        jest.clearAllMocks();
    });

    it('renders foundational fragrance details and filters out invalid accord strings', () => {
        render(
            <ResultCard
                result={mockFragrance}
                index={1}
                isAuthenticated={false}
            />
        );

        // verify title string formatting logic
        const heading = screen.getByRole('heading', { level: 3 });
        expect(heading).toHaveTextContent(/Plume Blanche 1901/i);
        expect(heading).toHaveTextContent(/lalique/i);
        expect(heading).toHaveTextContent(/2020/i);

        // verify standalon brand name paragraph renders
        const brandElements = screen.getAllByText(/lalique/i);
        expect(brandElements).toHaveLength(2);

        // verify rating strings and meta details render properly
        expect(screen.getByText(/Rating: 4.13/i)).toBeInTheDocument();
        expect(screen.getByText(/132 reviews/i)).toBeInTheDocument();
        expect(screen.getByText('Gender: unisex')).toBeInTheDocument();

        // verify valid accord badges render
        expect(screen.getByText('Almond')).toBeInTheDocument();
        expect(screen.getByText('Vanilla')).toBeInTheDocument();

        // verify that the custom logic successfully blocked the dummy 'none' accords from rendering
        expect(screen.queryByText('none')).not.toBeInTheDocument();

    });

    it('hides the heart button if unauthenticated, but shows it and responds to clicks when authenticated', async () => {
        const mockToggleFavorite = jest.fn();

        // scenario A: unauthenticated
        const { rerender } = render(
            <ResultCard
                result={mockFragrance}
                index={1}
                isAuthenticated={false}
            />
        );
        expect(screen.queryByRole('button', { name: /add to favorites/i })).not.toBeInTheDocument();

        // scenario B: authenticated and interacting
        rerender(
            <ResultCard
                result={mockFragrance}
                index={1}
                isAuthenticated={true}
                isFavorite={false}
                onToggleFavorite={mockToggleFavorite}
            />
        );
        const heartButton = screen.getByRole('button', { name: /add to favorites/i });
        expect(heartButton).toBeInTheDocument();

        // trigger interaction
        fireEvent.click(heartButton);
        
        await waitFor(() => {
            expect(mockToggleFavorite).toHaveBeenCalledWith(101);
        });
    });

    it('conditionally displays the similarity match score percentage based on configurations', () => {
        const { rerender } = render(
            <ResultCard
                result={mockFragrance}
                index={1}
                showScores={false}
            />
        );
        // should hide the raw text percentage value
        expect(screen.queryByText('(85.5%)')).not.toBeInTheDocument();

        rerender(
            <ResultCard
                result={mockFragrance}
                index={1}
                showScores={true}
            />
        );

        // raw text percentage should pop up
        expect(screen.getByText('(85.5%)')).toBeInTheDocument();
    });

    it('succesfully calls T5 engine generation on user click and updates profile text', async () => {
        const mockDescriptionResponse = { description: 'It smells like sweet powdered almonds and rich cream.'};
        (fragranceService.generateDescription as jest.Mock).mockResolvedValue(mockDescriptionResponse);

        render(<ResultCard result={mockFragrance} index={1} />);

        // verify the pre-generation action button is present
        const generateBtn = screen.getByRole('button', { name: /find out how this smells!/i });
        expect(generateBtn).toBeInTheDocument();

        // click the button to trigger generation
        fireEvent.click(generateBtn);

        // async cycle assertion
        await waitFor(() => {
            expect(fragranceService.generateDescription).toHaveBeenCalledWith("['almond', 'vanilla', 'musk']");
            expect(screen.getByText(/It smells like sweet powdered almonds and rich cream./i)).toBeInTheDocument();
            expect(screen.queryByRole('button', { name: /find out how this smells!/i })).not.toBeInTheDocument();
        });
    });
});
    