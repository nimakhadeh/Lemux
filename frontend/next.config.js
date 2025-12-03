/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: ['localhost'],
    unoptimized: true // برای توسعه - در تولید بهتر است بهینه شود
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*' // Django API
      },
      {
        source: '/ai/:path*',
        destination: 'http://localhost:8001/:path*' // FastAPI AI
      }
    ]
  },
  env: {
    BACKEND_URL: process.env.BACKEND_URL || 'http://localhost:8000',
    AI_API_URL: process.env.AI_API_URL || 'http://localhost:8001',
    APP_NAME: 'PropAnalyzer'
  }
}

module.exports = nextConfig