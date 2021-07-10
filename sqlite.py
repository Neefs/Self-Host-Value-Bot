import aiosqlite
import discord
import asyncio

async def insert_data(database: str=None, tables: list=None, checks: list=None) -> bool:
    db = await aiosqlite.connect("data/database.db")
    cur = await db.cursor()

    where_val = None

    if checks:
        where_val = "WHERE "
        for check, ans in checks:
            where_val += f"{check} = {ans} AND "
        where_val = where_val[:-4]

    table_names = ""
    table_values = []
    for name, value in tables:
        table_names += f"{name}, "
        table_values.append(value)
    
    table_names = table_names[:-2]

    try:
        if where_val:
            await db.execute(f"INSERT INTO {database} ({table_names}) VALUES ({('?, ' * len(tables))[:-2]}) {where_val}", tuple(table_values))
        else:
            await db.execute(f"INSERT INTO {database} ({table_names}) VALUES ({('?, ' * len(tables))[:-2]})", tuple(table_values))
        await db.commit()
    except Exception as e:
        raise e
        return False

    else:
        return True
    finally:
        await db.close()


async def update_data(database: str=None, tables: list=None, checks: list=None) -> bool:
    db = await aiosqlite.connect("data/database.db")
    cur = await db.cursor()

    where_val = None

    if checks:
        where_val = "WHERE "
        for check, ans in checks:
            where_val += f"{check} = {ans} AND "
        where_val = where_val[:-4]

    table_names = ""
    table_values = []
    for name, value in tables:
        table_names += f"{name} = ?,"
        table_values.append(value)
    
    table_names = table_names[:-1]

    try:
        if where_val:
            await db.execute(f"UPDATE {database} SET {table_names} {where_val}", tuple(table_values))
        else:
            await db.execute(f"UPDATE {database} SET {table_names}", tuple(table_values))
        await db.commit()
    except Exception as e:
        return False

    else:
        return True
    finally:
        await db.close()


async def read_data(database: str=None, tables: list=None, checks: list=None, order: list=None) -> tuple:
    db = await aiosqlite.connect("data/database.db")
    cur = await db.cursor()

    where_val = ""
    order_val = ""

    if checks:
        where_val = "WHERE "
        where_ans = []
        for check, ans in checks:
            where_val += f"{check} = ? AND "
            where_ans.append(ans)
        where_val = where_val[:-4]

    if order:
        order_val = "ORDER BY "
        for val in order:
            order_val += f"{val}, "
        order_val = order_val[:-2]
        

    table_names = ""
    for name in tables:
        table_names += f"{name},"
    
    table_names = table_names[:-1]

    try:
        if where_val:
            await cur.execute(f"SELECT {table_names} FROM {database} {where_val} {order_val}", tuple(where_ans))
            output = await cur.fetchall()
        else:
            await cur.execute(f"SELECT {table_names} FROM {database} {order_val}")
            output = await cur.fetchall()

    except Exception as e:
        pass
    else:
        return output
    finally:
        await db.close()

async def remove_data(database: str=None, checks: list=None) -> None:
    """IF NOT CHECKS DELTES EVERYTHING IN THE DATABASE TABLE"""
    db = await aiosqlite.connect("data/database.db")
    cur = await db.cursor()

    where_val = None

    if checks:
        where_val = "WHERE "
        where_ans = []
        for check, ans in checks:
            where_val += f"{check} = ? AND "
            where_ans.append(ans)
        where_val = where_val[:-4]

        try:
            await cur.execute(f"DELETE FROM {database} {where_val}", tuple(where_ans))
            await db.commit()
        
        except Exception as e:
            pass
        else:
            pass
        finally:
            await db.close()
    else:
        try:
            await cur.execute(f'DELETE FROM {database}')
            await db.commit()
        except Exception as e:
            pass
        else:
            pass
        finally:
            await db.close()