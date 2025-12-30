CREATE TABLE price_missions (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  user_id TEXT,
  asin TEXT,
  product_name TEXT,
  verdict TEXT,
  current_price FLOAT,
  target_price FLOAT,
  urgency INT
);