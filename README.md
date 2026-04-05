# Brazilian Sushi

<p align="center">
  <img alt="React" src="https://img.shields.io/badge/React-18-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" />
  <img alt="TypeScript" src="https://img.shields.io/badge/TypeScript-5-3178C6?style=for-the-badge&logo=typescript&logoColor=white" />
  <img alt="Vite" src="https://img.shields.io/badge/Vite-5-646CFF?style=for-the-badge&logo=vite&logoColor=white" />
  <img alt="Tailwind CSS" src="https://img.shields.io/badge/Tailwind_CSS-3-0F172A?style=for-the-badge&logo=tailwindcss&logoColor=38BDF8" />
  <img alt="Django" src="https://img.shields.io/badge/Django-5-092E20?style=for-the-badge&logo=django&logoColor=white" />
  <img alt="Django REST Framework" src="https://img.shields.io/badge/DRF-API-A30000?style=for-the-badge&logo=django&logoColor=white" />
  <img alt="SQLite" src="https://img.shields.io/badge/SQLite-Local-003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
  <img alt="Vercel" src="https://img.shields.io/badge/Vercel-Ready-000000?style=for-the-badge&logo=vercel&logoColor=white" />
</p>

Premium sushi delivery and takeout platform built for a realistic U.S.-market portfolio project, combining a polished mobile-first storefront with a production-minded Django API, customer accounts, order tracking, and staff operations.

## Links

- Live Demo: https://brazilian-sushi.vercel.app
- Repository: https://github.com/GugaValenca/brazilian-sushi

## Overview

Brazilian Sushi is designed as a premium restaurant ordering experience focused on delivery and pickup. The frontend emphasizes fast browsing, strong conversion flows, and refined presentation, while the backend supports real order orchestration, customer verification, promotions, reviews, and staff workflows.

The project was structured to stay interview-friendly: clear domain separation, practical REST APIs, realistic customer features, and maintainable local development without unnecessary enterprise complexity.

## Features

### Customer experience

- Premium home page with featured items, promotions, reviews, business highlights, and responsive CTAs
- Searchable menu with categories, combos, featured items, dietary/allergen labels, favorites, and add-to-cart flow
- Checkout with delivery or pickup, guest ordering, allergy notes, special instructions, and notification preferences
- Secure guest order tracking with a tracking token
- Account area with profile management, saved addresses, favorites, reorder flow, order history, and review submission for verified customers

### Business and staff operations

- Django admin plus a custom staff dashboard for live order queue management
- Quick status updates across received, confirmed, preparing, ready, out for delivery, and delivered states
- Verified customer controls tied to loyalty and manual verification workflows
- Review moderation, contact message queue, promotions, and coupon management
- Delivery zone support and API health endpoint for deployment checks

### SEO and platform readiness

- Page-level metadata for public and private routes
- `robots.txt`, `sitemap.xml`, and `site.webmanifest`
- Proper noindex strategy for checkout, auth, account, tracking, and staff routes
- Favicon configured through `public/favicon.ico`
- Vercel-ready frontend build with Django API kept local-first and production-extensible

## Screenshots

Screenshots were intentionally not versioned in this repository yet to avoid low-quality or outdated captures. The UI currently includes polished experiences for the home page, menu, checkout, account area, and staff dashboard.

## Tech Stack

### Frontend

- React
- TypeScript
- Vite
- Tailwind CSS
- shadcn/ui
- TanStack Query
- React Router
- Framer Motion

### Backend

- Django
- Django REST Framework
- Simple JWT
- SQLite for local development
- PostgreSQL-ready environment configuration for production

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/GugaValenca/brazilian-sushi.git
cd brazilian-sushi
```

### 2. Install frontend dependencies

```bash
npm install
```

### 3. Create the local environment file

```bash
cp .env.example .env
```

On Windows PowerShell, you can use:

```powershell
Copy-Item .env.example .env
```

### 4. Run Django migrations and seed the menu

```bash
python manage.py migrate
python manage.py seed_brazilian_sushi
```

## Usage

### Frontend

```bash
npm run dev:frontend
```

Frontend URL: `http://127.0.0.1:8080`

### Backend

```bash
npm run dev:backend
```

Backend URL: `http://127.0.0.1:8010`

Health check: `http://127.0.0.1:8010/api/health/`

### Validation

```bash
npm run lint
npm run build
npm run check:backend
npm run test:backend
```

## Production Environment

For a professional Vercel deployment with the Django API enabled, configure these variables in the Vercel project:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG=false`
- `DJANGO_ALLOWED_HOSTS`
- `CORS_ALLOWED_ORIGINS`
- `CSRF_TRUSTED_ORIGINS`
- `DATABASE_URL`
- `DB_SSLMODE=require`
- `DB_CONN_MAX_AGE=60`

The frontend now defaults to `/api` in production, so a separate `VITE_API_BASE_URL` is not required unless you intentionally host the API on another domain.

## Project Structure

```text
.
|-- accounts/
|-- backend/
|-- marketing/
|-- menu/
|-- orders/
|-- public/
|-- src/
|   |-- components/
|   |-- contexts/
|   |-- hooks/
|   |-- lib/
|   |-- pages/
|-- manage.py
|-- package.json
```

## Technical Highlights / What I Learned

- Built a realistic fullstack ordering flow with clear separation between storefront, customer account, and staff operations
- Applied practical security decisions such as token-based guest tracking instead of exposing raw order access
- Kept the stack explainable and portfolio-friendly while still covering meaningful product concerns like moderation, segmentation, and operational dashboards
- Improved public readiness with route-aware SEO metadata and indexability controls

## Future Improvements

- Connect transactional email and SMS providers for live notification delivery
- Add payment processing for a full online checkout flow
- Extend analytics and restaurant reporting for revenue, delivery time, and campaign performance
- Add image-based screenshots and richer admin insights once final UI approval is complete

## Contributing

This repository is currently maintained as a portfolio project, but suggestions and improvements are welcome through issues or pull requests.

## License

This project is available under the MIT License. Add a `LICENSE` file before public release if you want the repository to be explicitly licensed.

## Contact

- GitHub: https://github.com/GugaValenca
- LinkedIn: https://www.linkedin.com/in/gustavo-valenca
- Email: contact through GitHub profile
