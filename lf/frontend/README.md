# Spotify AI Workshop - Frontend

A React + TypeScript frontend for generating AI-powered Spotify playlist covers.

## 🚀 Getting Started

### Prerequisites
- Node.js (v18 or higher)
- npm or yarn
- Backend server running on port 5000

### Installation

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Start the development server**
   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:3000`

## 📁 Project Structure

```
src/
├── components/       # Reusable components
│   ├── Navbar/
│   ├── PlaylistCard/
│   └── Spinner/
├── pages/           # Page components
│   ├── PlaylistsPage.tsx
│   └── GeneratorPage.tsx
├── model/           # TypeScript interfaces
├── styles/          # Global styles
├── App.tsx          # Main app component
└── main.tsx         # Entry point
```

## 🎨 Features

- Browse your Spotify playlists
- View tracks in each playlist
- Generate AI-powered cover images using DALL-E 3
- Responsive design with Tailwind CSS

## 🛠️ Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run lint` - Run ESLint
- `npm run preview` - Preview production build

## 🔌 API Integration

The frontend connects to the backend API running on `http://localhost:5000`:

- `GET /api/get-playlist` - Fetch user playlists
- `GET /api/get-tracks?playlist_id={id}` - Get tracks for a playlist
- `GET /api/generate-cover?playlist_id={id}` - Generate AI cover image

## 🎓 Workshop Tasks

This project is designed for learning. Key areas to explore:

1. **Component structure** - How React components are organized
2. **State management** - Using useState and useEffect hooks
3. **API integration** - Making HTTP requests with axios
4. **Routing** - Navigation with react-router-dom
5. **Styling** - CSS modules and Tailwind CSS

## 📝 Notes

- Make sure the backend server is running before starting the frontend
- The Vite proxy configuration forwards `/api/*` requests to `http://localhost:5000`
