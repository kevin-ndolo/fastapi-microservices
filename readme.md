# 🧰 Inventory Microservice App

A demo-ready inventory/order system powered by **FastAPI**, **Redis JSON DB**, **Redis Streams**, and a **React frontend**. Built to highlight clean microservice separation, async background processing, and a streamlined UI layer.

---

## 🚀 Tech Stack

### Backend:
- **FastAPI** – lightning-fast Python web framework
- **Redis OM for Python** – handles Redis HashModel persistence
- **Redis Streams** – event-driven coordination between services
- **CORS Middleware**, **BackgroundTasks**, environment-based config

### Frontend:
- **React (v18+)** – functional components & hooks
- **React Router (v6)** – client-side routing
- **Bootstrap CSS** – responsive layout and UI polish

---

## 🗂️ Project Structure

```
.
├── .env
├── .gitignore
├── requirements.txt
├── README.md
├── venv/
├── inventory/
│   ├── consumer.py
│   ├── main.py
│   └── __pycache__/
├── payment/
│   ├── consumer.py
│   ├── main.py
│   └── __pycache__/
└── inventory-frontend/
    ├── package.json
    ├── package-lock.json
    ├── public/
    ├── README.md
    └── src/
        ├── App.js
        ├── index.js
        └── components/
            ├── Product.js
            ├── Wrapper.js
            └── ...
```

---

## ⚙️ Getting Started

### 🖥 Backend Setup

1. Create a `.env` file in the root directory:
   ```env
   REDIS_HOST=<your_redis_host>
   REDIS_PORT=<your_port>
   REDIS_USERNAME=default
   REDIS_PASSWORD=<your_password>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run all backend services (in separate terminals):
   ```bash
   uvicorn inventory.main:app --reload
   uvicorn payment.main:app --reload
   python -m inventory.consumer
   python -m payment.consumer
   ```

---

### 💻 Frontend Setup

1. Navigate into the React app:
   ```bash
   cd inventory-frontend
   npm install
   npm start
   ```

2. React UI will be available at [http://localhost:3000](http://localhost:3000)

---

## 🧭 Manual Frontend Navigation

Since navigation links are partially implemented, here are the direct paths:

| Path      | Function                |
|-----------|-------------------------|
| `/`       | View & delete products  |
| `/create` | Create a new product    |
| `/orders` | View orders (read-only) |

📌 Use your browser address bar to manually navigate if links are missing.

---

## 🔄 Data Flow Overview

- **Product Created** → Saved to Redis via `inventory/main.py`
- **Order Created** → Triggers background task → Sends `order_completed` event to Redis Stream
- **Inventory Consumer** → Listens to stream → Decrements quantity or emits `refund_order`
- **Payment Consumer** → Listens to refund stream → Marks orders as "refunded"

---

## ✅ Completed Features

- [x] Product list, create & delete from frontend
- [x] Redis-backed persistence (no SQL required)
- [x] Event-driven flow between microservices
- [x] React UI tied to FastAPI endpoints
- [x] Postman-verified endpoints for demo/testing

---

## 📝 TODOs / Improvements

- [ ] Add working links to `/create` and `/orders` in the sidebar (`Wrapper.js`)
- [ ] Swap all static `<a href="#">` for React Router’s `<Link to="...">`
- [ ] Integrate order creation into frontend
- [ ] Toast notifications on success/error
- [ ] Add form validation and input feedback

---

## 📬 API Endpoints

### Inventory Service (`http://localhost:8000`)
| Method | Endpoint           | Description              |
|--------|--------------------|--------------------------|
| GET    | `/products/`       | List all products        |
| POST   | `/products`        | Create new product       |
| GET    | `/products/{id}`   | Get single product       |
| DELETE | `/products/{id}`   | Delete product           |

### Payment Service (`http://localhost:8001`)
| Method | Endpoint         | Description                  |
|--------|------------------|------------------------------|
| POST   | `/orders`        | Create order (triggers event)|
| GET    | `/orders/{id}`   | Retrieve order info          |

---

🧑‍💻 Built with care by Kevin  
🏁 Demo