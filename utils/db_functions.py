from database import create_connection

def get_data(table_name, columns="*", where=None, order_by=None, limit=None):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = f"SELECT {columns} FROM {table_name}"
    if where:
        query += f" WHERE {where}"
    if order_by:
        query += f" ORDER BY {order_by}"
    if limit:
        query += f" LIMIT {limit}"
    
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results

def save_data(table_name, data_dict):
    conn = create_connection()
    cursor = conn.cursor()
    columns = ", ".join(data_dict.keys())
    placeholders = ", ".join(["%s"] * len(data_dict))
    values = tuple(data_dict.values())
    
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    try:
        cursor.execute(query, values)
        conn.commit()
        return True
    except Exception as e:
        print(f"Error save_data: {e}")
        return False
    finally:
        cursor.close()

def update_data(table_name, data_dict, where_clause):
    conn = create_connection()
    cursor = conn.cursor()
    
    set_clause = ", ".join([f"{k} = %s" for k in data_dict.keys()])
    values = tuple(data_dict.values())
    
    query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
    try:
        cursor.execute(query, values)
        conn.commit()
        return True
    except Exception as e:
        print(f"Error update_data: {e}")
        return False
    finally:
        cursor.close()

def delete_data(table_name, where_clause):
    conn = create_connection()
    cursor = conn.cursor()
    
    query = f"DELETE FROM {table_name} WHERE {where_clause}"
    try:
        cursor.execute(query)
        conn.commit()
        return True
    except Exception as e:
        print(f"Error delete_data: {e}")
        return False
    finally:
        cursor.close()

def bulk_insert(table_name, data_list):
    if not data_list:
        return False
    
    conn = create_connection()
    cursor = conn.cursor()
    
    columns = ", ".join(data_list[0].keys())
    placeholders = ", ".join(["%s"] * len(data_list[0]))
    
    values = [tuple(d.values()) for d in data_list]
    
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    
    try:
        cursor.executemany(query, values)
        conn.commit()
        return True
    except Exception as e:
        print(f"Error bulk_insert: {e}")
        return False
    finally:
        cursor.close()
