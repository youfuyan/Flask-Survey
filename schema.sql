CREATE TABLE survey_responses (
  id SERIAL PRIMARY KEY,
  customer TEXT NOT NULL,
  breeder TEXT NOT NULL,
  rating INTEGER NOT NULL,
  recommend BOOLEAN,
  comments TEXT,
  timestamp TIMESTAMP DEFAULT NOW()
);

ALTER TABLE survey_responses ADD CONSTRAINT unique_customer UNIQUE (customer);
