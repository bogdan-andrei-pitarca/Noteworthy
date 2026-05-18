import logging
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List

from database.db_session import get_connection
from routers.auth import get_current_user_id
from routers.search import FragranceBase, FragranceSearchResult

router = APIRouter(prefix="/favorites", tags=["User Favorites"])

@router.post("/{embedding_id}", status_code=status.HTTP_201_CREATED)
async def add_favorite(embedding_id: int, user_id: int = Depends(get_current_user_id)):
    """Save a fragrance to the user's favorites."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
        # check if fragrance exists
            cur.execute("SELECT embedding_id FROM fragrances WHERE embedding_id = %s", (embedding_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Fragrance not found")
            
            # insert it (the ON CONFLICT prevents crashing if they try to add the same one twice)
            cur.execute(
                """
                INSERT INTO favorites (user_id, embedding_id)
                VALUES (%s, %s)
                ON CONFLICT (user_id, embedding_id) DO NOTHING
                """,
                (user_id, embedding_id)
            )
            conn.commit()
            return {"message": "Fragrance added to favorites"}
    except Exception as e:
        raise
    except Exception as e:
        conn.rollback()
        logging.error(f"Error adding favorite: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        conn.close()


@router.get("/", response_model=List[FragranceBase])
async def get_favorites(user_id: int = Depends(get_current_user_id)):
    """Retrieve the user's favorite fragrances."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT f.embedding_id, f.perfume_name, f.brand, f.gender, 
                       f.launch_year, f.rating_value, f.rating_count, f.url, 
                       f.main_accord_1, f.main_accord_2, f.main_accord_3, 
                       f.main_accord_4, f.main_accord_5, f.all_notes
                FROM fragrances f
                JOIN favorites fav ON f.embedding_id = fav.embedding_id
                WHERE fav.user_id = %s
                ORDER BY fav.added_at DESC
                """,
                (user_id,)
            )
            columns = [desc[0] for desc in cur.description]

            favorites = [dict(zip(columns, row)) for row in cur.fetchall()]
            return favorites
    except Exception as e:
        logging.error(f"Error retrieving favorites: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        conn.close()


@router.delete("/{embedding_id}")
async def remove_favorite(embedding_id: int, user_id: int = Depends(get_current_user_id)):
    """Removes a fragrance from the user's favorites"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM favorites WHERE user_id = %s AND embedding_id = %s",
                (user_id, embedding_id)
            )
            conn.commit()
            return {"message": "Fragrance removed from favorites"}
    except Exception as e:
        conn.rollback()
        logging.error(f"Error removing favorite: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        conn.close()