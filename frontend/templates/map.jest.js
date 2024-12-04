const { filterBathroomsByGender, calculateDistance } = require('./functions'); // Assuming functions are modularized

describe('filterBathroomsByGender', () => {
    const bathrooms = [
        { id: 1, gender: 'M' },
        { id: 2, gender: 'W' },
        { id: 3, gender: 'N' },
    ];

    it('should return all bathrooms when selectedGender is "all"', () => {
        const result = filterBathroomsByGender(bathrooms, 'all');
        expect(result).toEqual(bathrooms);
    });

    it('should filter only male bathrooms when selectedGender is "M"', () => {
        const result = filterBathroomsByGender(bathrooms, 'M');
        expect(result).toEqual([{ id: 1, gender: 'M' }, { id: 3, gender: 'N' }]);
    });

    it('should filter only female bathrooms when selectedGender is "W"', () => {
        const result = filterBathroomsByGender(bathrooms, 'W');
        expect(result).toEqual([{ id: 2, gender: 'W' }, { id: 3, gender: 'N' }]);
    });

    it('should filter only neutral bathrooms when selectedGender is "N"', () => {
        const result = filterBathroomsByGender(bathrooms, 'N');
        expect(result).toEqual([{ id: 3, gender: 'N' }]);
    });
});

describe('calculateDistance', () => {
    it('should calculate the distance between two coordinates correctly', () => {
        const lat1 = 44.0464;
        const lon1 = -123.0777;
        const lat2 = 44.0501;
        const lon2 = -123.0955;

        const distance = calculateDistance(lat1, lon1, lat2, lon2);
        expect(distance).toBeCloseTo(1.03, 2); // Within 2 decimal places
    });

    it('should return 0 for the same coordinates', () => {
        const lat = 44.0464;
        const lon = -123.0777;

        const distance = calculateDistance(lat, lon, lat, lon);
        expect(distance).toBe(0);
    });
});
