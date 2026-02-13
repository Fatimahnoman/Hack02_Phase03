/** @type {import('next').NextConfig} */
const nextConfig = {
  trailingSlash: false,
  images: {
    unoptimized: true
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'https://fatimahnoman-phase-three.hf.space',
  },
  // Remove the custom rewrites that might interfere with Vercel's asset serving
  // The API calls should be handled directly by the frontend using NEXT_PUBLIC_API_URL
}

module.exports = nextConfig