from starlette.requests import Request
import requests, time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel
import os
from dotenv import load_dotenv



load_dotenv()  # Load environment variables from .env


REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
REDIS_USERNAME = os.getenv("REDIS_USERNAME")                 
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")


# This should be a different database, using this to avoid paying for multiple Redis instances in the free tier
redis = get_redis_connection(
    host=REDIS_HOST,
    port=REDIS_PORT,
    username=REDIS_USERNAME,
    password=REDIS_PASSWORD,
    decode_responses=True
)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000/"],  # Allows localhost for development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str # e.g., "pending", "completed", "refunded"

    class Meta:
        database = redis



@app.get("/")
async def root():
    return {"message": "Hello From Payment Service!"}



@app.get("/orders/{pk}")
def get(pk: str):
    return Order.get(pk)  # Retrieve the order by primary key   



@app.post("/orders/") 
async def create(request: Request, background_tasks: BackgroundTasks): # id, quantity
    body = await request.json()


    
    # req = requests.get(f"http://product:8000/products/%s" % body["id"])
    req = requests.get(f"http://localhost:8000/products/{body['id']}")

    product = req.json()    

    order = Order(  
        product_id=body["id"],
        price=product["price"],
        fee=0.2 * product["price"], 
        total= 1.2 * product["price"],
        quantity=body["quantity"],
        status="pending"
    )

    order.save()  # Save the order to Redis 

    background_tasks.add_task(order_completed, order)  # Add the order completion task to the background    

    

    return order  # Return the order object






def order_completed(order: Order):
    time.sleep(5)  # Simulate some processing time
    order.status = "completed"
    order.save()
    
    redis.xadd("order_completed", order.dict(), "*")  # Add the completed order to the Redis stream
      
