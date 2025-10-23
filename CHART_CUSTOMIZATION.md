# Chart Customization Feature

## Overview
The dashboard now allows users to dynamically select the number of items displayed in both the pie chart and bar chart.

## Features Added

### 1. **Dynamic Country Pie Chart**
- **Location**: Top left chart on dashboard
- **Options**: Top 3, 5, 10, 15, or 20 countries
- **Default**: Top 5 countries
- **Functionality**: Shows countries by total views with automatic color generation

### 2. **Dynamic Channel Bar Chart**
- **Location**: Top right chart on dashboard
- **Options**: Top 5, 10, 15, 20, 30, or 50 channels
- **Default**: Top 10 channels
- **Functionality**: Shows channels by subscriber count

## How to Use

### Changing Chart Display
1. Navigate to the dashboard at `http://127.0.0.1:5000/dashboard`
2. Look for the dropdown selectors above each chart
3. Select your desired number of items (e.g., "Top 15", "Top 20")
4. The page will automatically reload with the updated chart

### URL Parameters
You can also directly use URL parameters:
```
http://127.0.0.1:5000/dashboard?num_channels=20&num_countries=10
```
- `num_channels`: Number of channels to display (3-50)
- `num_countries`: Number of countries to display (3-20)

### Combining with Country Filter
All features work together seamlessly:
```
http://127.0.0.1:5000/dashboard?num_channels=15&num_countries=10&country=India
```

## Technical Implementation

### Backend Changes (app.py)
```python
# Get user-selected numbers with validation
num_channels = request.args.get('num_channels', 10, type=int)
num_countries = request.args.get('num_countries', 5, type=int)

# Ensure valid ranges
num_channels = max(3, min(num_channels, 50))  # 3-50
num_countries = max(3, min(num_countries, 20))  # 3-20

# Query data dynamically
top_channels = df.nlargest(num_channels, 'subscribers')
country_views = df.groupby('country')['views'].sum().nlargest(num_countries)
```

### Frontend Features (dashboard.html)

#### 1. **Smart Color Generation**
```javascript
function generateColors(count) {
    // Uses 20 predefined colors
    // Generates additional colors using HSL golden angle for counts > 20
    // Ensures visually distinct colors
}
```

#### 2. **Chart Update Function**
```javascript
function updateChart(chartType) {
    // Preserves existing filters (country selection)
    // Updates URL parameters
    // Reloads page with new chart data
}
```

#### 3. **Responsive Dropdown Selectors**
- Styled to match dashboard theme
- Gradient borders on hover/focus
- Smooth transitions

## Benefits

### 1. **Flexibility**
- Users can analyze different data ranges
- Suitable for both overview and detailed analysis

### 2. **Performance**
- Backend validates ranges (3-50 channels, 3-20 countries)
- Prevents excessive data loading

### 3. **User Experience**
- Intuitive dropdown interface
- Automatic color generation for any count
- Maintains context (country filter persists)

### 4. **Visual Quality**
- 20 carefully selected gradient colors
- HSL-based generation for additional colors
- Even color distribution using golden angle (137.5°)

## Color Palette
The dynamic color generation uses:
- **Base Palette**: 20 predefined gradient colors
  - Purple: `#667eea`, `#5f27cd`
  - Pink: `#f093fb`, `#fa709a`, `#ff9ff3`, `#f368e0`
  - Blue: `#4facfe`, `#45b7d1`, `#54a0ff`, `#48dbfb`
  - Green: `#43e97b`, `#1dd1a1`, `#4ecdc4`
  - Orange/Yellow: `#f7b731`, `#feca57`, `#ff9f43`
  - Red: `#ff6b6b`, `#ee5a6f`, `#c44569`
  - Cyan: `#00d2d3`

- **Extended Colors**: HSL-based generation for counts > 20

## Example Use Cases

### Case 1: Quick Overview
```
num_channels=5, num_countries=3
```
Perfect for presentations - shows only top performers

### Case 2: Detailed Analysis
```
num_channels=50, num_countries=20
```
Comprehensive view for in-depth analysis

### Case 3: Regional Focus
```
num_channels=20, num_countries=10, country=United States
```
Combined view with geographic filter

## Future Enhancements (Optional)
- [ ] Add "All" option for both charts
- [ ] Export chart data to CSV
- [ ] Save user preferences in localStorage
- [ ] Add animation transitions when changing chart size
- [ ] Enable chart zoom/pan for large datasets
- [ ] Add chart type switcher (pie/doughnut/bar/line)

## Notes
- Charts maintain responsive behavior on mobile devices
- All changes preserve the existing country filter selection
- Color generation ensures accessibility and visual distinction
- Backend validation prevents invalid ranges
