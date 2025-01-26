from fastapi import APIRouter, HTTPException
from app.services.bundling_service import BundleService
from app.services.redis_service import RedisService

router = APIRouter()

@router.get("/generate-bundle/{file_path}")
def generate_bundle(file_path: str, repo_id: str):
    try:
        redis_service = RedisService()
        bundling_service = BundleService(repo_id, redis_service.redis_client)

        # Generate bundle
        bundle_metadata = bundling_service.generate_bundle_for_ui(file_path)
        return {"bundle": bundle_metadata}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
