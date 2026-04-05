# Brazilian Sushi

<p align="center">
  <img alt="React" src="https://img.shields.io/badge/React-18-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" />
  <img alt="TypeScript" src="https://img.shields.io/badge/TypeScript-5-3178C6?style=for-the-badge&logo=typescript&logoColor=white" />
  <img alt="Vite" src="https://img.shields.io/badge/Vite-5-646CFF?style=for-the-badge&logo=vite&logoColor=white" />
  <img alt="Tailwind CSS" src="https://img.shields.io/badge/Tailwind_CSS-3-0F172A?style=for-the-badge&logo=tailwindcss&logoColor=38BDF8" />
  <img alt="Django" src="https://img.shields.io/badge/Django-5-092E20?style=for-the-badge&logo=django&logoColor=white" />
  <img alt="Django REST Framework" src="https://img.shields.io/badge/DRF-API-A30000?style=for-the-badge&logo=django&logoColor=white" />
  <img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-Neon-1D4ED8?style=for-the-badge&logo=postgresql&logoColor=white" />
  <img alt="Vercel" src="https://img.shields.io/badge/Vercel-Production-000000?style=for-the-badge&logo=vercel&logoColor=white" />
</p>

<p align="center">
  Premium sushi delivery and takeout platform built as a realistic fullstack portfolio project for the U.S. market, combining a polished storefront, production-minded backend, customer accounts, order tracking, promotions, and staff operations.
</p>

<p align="center">
  <a href="https://brazilian-sushi.vercel.app">
    <img alt="Live Demo" src="https://img.shields.io/badge/Live_Demo-Brazilian_Sushi-B22222?style=for-the-badge&logo=vercel&logoColor=white" />
  </a>
  <a href="https://github.com/GugaValenca/BRAZILIAN-SUSHI">
    <img alt="Repository" src="https://img.shields.io/badge/Repository-GitHub-111827?style=for-the-badge&logo=github&logoColor=white" />
  </a>
</p>

## 🍣 About The Project

Brazilian Sushi was designed as a premium restaurant ordering experience focused on delivery and pickup. The product balances refined branding, conversion-oriented UX, and operational practicality, covering the customer journey from menu browsing to checkout, tracking, account management, and staff-side order handling.

The project was intentionally built to stay realistic and interview-friendly: modern frontend architecture, a clean Django API, practical security decisions, and a feature set that feels credible for a professional portfolio without unnecessary enterprise complexity.

## ✨ Key Features

### 🛍️ Ordering Experience

- Premium home page with featured items, promotions, reviews, business highlights, and clear conversion paths
- Searchable menu with categories, combos, favorites, dietary and allergen labels, and add-to-cart flow
- Checkout flow with delivery or pickup, guest ordering, allergy notes, special instructions, and notification preferences
- Secure guest order tracking through a tracking token
- Customer account with saved addresses, favorites, order history, profile settings, and review submission for verified customers

### 🧑‍🍳 Restaurant Operations

- Django admin plus a custom staff dashboard for queue visibility and quick status updates
- Order lifecycle support across received, confirmed, preparing, ready, out for delivery, and delivered states
- Verified customer controls tied to loyalty and operational workflows
- Review moderation, promotions, coupons, and contact-message handling
- Health endpoint and production-ready environment setup for deployment verification

### 🚀 SEO and Production Readiness

- Route-aware metadata strategy for public and private pages
- `robots.txt`, `sitemap.xml`, and `site.webmanifest`
- Noindex strategy for checkout, account, tracking, auth, and staff pages
- Custom favicon configured in `public/favicon.ico`
- Vercel deployment with Django API support and PostgreSQL-backed production setup

## 📸 Application Screenshots

Add your final screenshots to `docs/screenshots/` using the file names below:

- `docs/screenshots/home-page.png`
- `docs/screenshots/menu-page.png`
- `docs/screenshots/checkout-page.png`
- `docs/screenshots/account-page.png`
- `docs/screenshots/staff-dashboard.png`

README-ready links:

```md
![Home Page](docs/screenshots/home-page.png)
![Menu Page](docs/screenshots/menu-page.png)
![Checkout Page](docs/screenshots/checkout-page.png)
![Account Page](docs/screenshots/account-page.png)
![Staff Dashboard](docs/screenshots/staff-dashboard.png)
```

## 🛠 Technology Stack

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
- PostgreSQL with Neon in production
- SQLite for local development

### Deployment

- Vercel
- Neon PostgreSQL

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/GugaValenca/BRAZILIAN-SUSHI.git
cd BRAZILIAN-SUSHI
```

### 2. Install frontend dependencies

```bash
npm install
```

### 3. Create the local environment file

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

### 4. Run migrations and seed the menu

```bash
python manage.py migrate
python manage.py seed_brazilian_sushi
```

## ▶️ Running The Project

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

## 🧱 Project Structure

```text
.
|-- accounts/
|-- api/
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
|-- requirements.txt
|-- vercel.json
```

## 🧠 Technical Highlights

- Built a realistic fullstack ordering flow with clear separation between storefront, customer account, and staff operations
- Applied practical security decisions such as token-based guest tracking instead of exposing raw order access
- Designed a portfolio-ready product that stays explainable in interviews while still covering meaningful business workflows
- Strengthened production readiness with deployment validation, public metadata strategy, and PostgreSQL-backed configuration

## 🔮 Future Improvements

- Integrate transactional email and SMS providers for live customer notifications
- Add payment processing for a fully online checkout flow
- Expand reporting around delivery performance, campaign results, and revenue trends
- Add curated README screenshots once the final visual capture set is prepared

## 🤝 Contributing

This repository is maintained as a portfolio project, but thoughtful suggestions and improvements are welcome through issues or pull requests.

## 📄 License

This project is available under the MIT License. Add a `LICENSE` file if you want the repository to be explicitly licensed for public distribution.

## 📬 Contact

<p align="center">
  <a href="https://github.com/GugaValenca">
    <img alt="GitHub" src="https://img.shields.io/badge/GitHub-GugaValenca-181717?style=for-the-badge&logo=github&logoColor=white" />
  </a>
  <a href="https://www.linkedin.com/in/gustavo-valenca">
    <img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-Gustavo_Valenca-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" />
  </a>
  <a href="https://brazilian-sushi.vercel.app">
    <img alt="Live Demo" src="https://img.shields.io/badge/Live_Demo-Brazilian_Sushi-B22222?style=for-the-badge&logo=vercel&logoColor=white" />
  </a>
</p>
