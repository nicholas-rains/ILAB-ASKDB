# schema.py

def get_schema():
    """
    Returns the database schema information as a formatted string.
    """
    return """
    Table: account
      - reporting_date (timestamp without time zone) [Primary Key]
      - account_id (integer) [Primary Key]
      - account_classification (text)
      - account_source (text)
      - account_status (text)
      - prin_outstanding_balance (double precision)
    Constraints:
      - Primary Key: (reporting_date, account_id)
      - No Foreign Keys

    Table: account_x_customer_rltnp
      - reporting_date (timestamp without time zone) [Primary Key]
      - account_id (integer) [Primary Key]
      - customer_id (integer) [Primary Key]
    Constraints:
      - Primary Key: (reporting_date, account_id, customer_id)
      - Foreign Key: (customer_id, reporting_date) -> (customer.customer_id, customer.reporting_date)

    Table: customer
      - reporting_date (timestamp without time zone) [Primary Key]
      - customer_id (integer) [Primary Key]
      - customer_type (text)
      - cntry_of_ctnzshp (text)
      - us_resncy_state (text)
      - wh8_ind (text)
      - parent_cust_id (integer)
      - birth_date (timestamp without time zone)
    Constraints:
      - Primary Key: (reporting_date, customer_id)

    Table: customer_details
      - customer_id (integer) [Primary Key]
      - first_name (varchar(50))
      - last_name (varchar(50))
      - add_ln_1 (varchar(100))
      - add_ln_2 (varchar(100))
      - city (varchar(50))
      - state (varchar(2))
      - zip (varchar(10))
      - ssn (varchar(15))
      - home_phone (varchar(15))
      - mobile_phone (varchar(15))
    Constraints:
      - Primary Key: (customer_id)

    Table: customer_idntfctn
      - reporting_date (timestamp without time zone)
      - customer_id (integer)
      - idntfctn_type (text)
      - idntfctn_nmbr (double precision)
    Constraints:
      - Foreign Key: (customer_id, reporting_date) -> (customer.customer_id, customer.reporting_date)
      - No Primary Key

    Table: deposit
      - reporting_date (timestamp without time zone) [Primary Key]
      - account_id (integer) [Primary Key]
      - account_source (text)
      - account_status (text)
      - avg_balance_amt (double precision)
      - opening_dp_amt (integer)
      - dp_ar_type_desc (text)
      - funds_own_type_desc (text)
    Constraints:
      - Primary Key: (reporting_date, account_id)
      - No Foreign Keys
    """
