# Evolution of Todo Frontend

This is the frontend for the Evolution of Todo application, deployed on Vercel and connected to a backend hosted on Hugging Face Spaces.

## Overview

This is a Next.js application that provides a user interface for managing tasks and interacting with AI-powered agents. The frontend communicates with a backend API for all data operations.

## Features

- User authentication (sign up/sign in)
- Task management (create, update, delete)
- AI-powered chat interface
- Dashboard for task overview

## Tech Stack

- Next.js 14
- React 18
- TypeScript
- Axios for API calls
- Tailwind CSS (or your chosen styling solution)

## Environment Variables

This application uses the following environment variable:

- `NEXT_PUBLIC_API_URL` - The URL of the backend API (defaults to the deployed Hugging Face backend)

## Deployment

This application is deployed on Vercel. The deployment automatically connects to the backend API hosted at https://fatimahnoman-phase-three.hf.space

### To deploy on Vercel:

1. Fork or clone this repository
2. Go to [Vercel](https://vercel.com) and create an account
3. Import your repository
4. Add the environment variable:
   - `NEXT_PUBLIC_API_URL`: Set to `https://fatimahnoman-phase-three.hf.space`
5. Deploy!

## API Integration

The application connects to the backend API through:

1. An API service file (`src/services/api.ts`) that handles all HTTP requests
2. Automatic addition of authentication tokens to requests
3. Error handling and redirection for unauthorized access

## Scripts

- `npm run dev` - Start the development server
- `npm run build` - Build the application for production
- `npm start` - Start the production server
- `npm run lint` - Run ESLint

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request