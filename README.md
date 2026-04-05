# Brazilian Sushi

Premium sushi delivery and takeout web experience built with React, TypeScript, and Django REST Framework.

## Repository

- Frontend and API live in the same repository for local-first development.
- Repository: https://github.com/GugaValenca/brazilian-sushi-hub

## Stack

- Frontend: React, TypeScript, Vite, Tailwind CSS, shadcn/ui
- Backend: Django, Django REST Framework, Simple JWT
- Database: SQLite for local development, PostgreSQL-ready through environment variables

## Features

- Premium mobile-first restaurant interface
- Menu categories, featured items, combos, filters, and add-to-cart-ready backend models
- Delivery or pickup checkout flow support
- Guest checkout and authenticated customer accounts
- Saved addresses, favorites, communication preferences, and order history
- Verified customer workflow with loyalty and pickup-based verification rules
- Review submission restricted to verified customers with admin approval flow
- Promotions, coupons, contact messages, and delivery zones
- Staff-friendly order queue and admin dashboard support
- API health endpoint for deployment checks

## Local Development

### Frontend

```bash
npm run dev:frontend
```

Runs at `http://127.0.0.1:8080`.

### Backend

```bash
python manage.py migrate
python manage.py seed_brazilian_sushi
npm run dev:backend
```

Runs at `http://127.0.0.1:8010`.

### Backend checks

```bash
npm run check:backend
npm run test:backend
```

## Environment

Use `.env.example` as the reference for local configuration.

Important variables:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `CORS_ALLOWED_ORIGINS`
- `CSRF_TRUSTED_ORIGINS`
- `VITE_API_BASE_URL`

## API Areas

- `/api/health/`
- `/api/accounts/`
- `/api/menu/`
- `/api/orders/`
- `/api/marketing/`
- `/admin/`

## Notes

- `public/favicon.ico` is the project favicon used by the frontend.
- No credentials, secrets, or local-only environment files should be committed.
- The backend is structured to keep the current frontend identity intact while making the project production-ready to evolve.
