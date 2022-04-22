import os
from typing import Optional

from app.common.infrastructure.data.repositories.mongo_repository_base import MongoRepositoryBase
from app.ingest.domain.models.ingest.depositing_application import DepositingApplication
from app.ingest.domain.models.ingest.ingest import Ingest
from app.ingest.domain.models.ingest.ingest_status import IngestStatus
from app.ingest.domain.repositories.ingest_repository import IIngestRepository
from app.ingest.infrastructure.data.repositories.db_connection_params import DbConnectionParams


class IngestRepository(IIngestRepository, MongoRepositoryBase):
    def save(self, ingest: Ingest) -> None:
        db = self._get_database()
        db.ingests.insert_one(self.__transform_ingest_to_mongo_dict(ingest))

    def get_by_package_id(self, package_id: str) -> Optional[Ingest]:
        db = self._get_database()
        ingest_mongo_dict = db.ingests.find_one({"package_id": package_id})
        if ingest_mongo_dict is None:
            return None
        return self.__transform_mongo_dict_to_ingest(ingest_mongo_dict)

    def _get_db_connection_params(self) -> DbConnectionParams:
        return DbConnectionParams(
            db_hosts=[os.getenv('MONGODB_HOST_1'), os.getenv('MONGODB_HOST_2'), os.getenv('MONGODB_HOST_3')],
            db_port=int(os.getenv('MONGODB_PORT')),
            db_name=os.getenv('MONGODB_DB_NAME'),
            db_user=os.getenv('MONGODB_USER'),
            db_password=os.getenv('MONGODB_PASSWORD'),
        )

    def __transform_ingest_to_mongo_dict(self, ingest: Ingest) -> dict:
        return {
            "package_id": ingest.package_id,
            "s3_path": ingest.s3_path,
            "s3_bucket_name": ingest.s3_bucket_name,
            "admin_metadata": ingest.admin_metadata,
            "status": ingest.status.value,
            "depositing_application": ingest.depositing_application.value
        }

    def __transform_mongo_dict_to_ingest(self, mongo_dict: dict) -> Ingest:
        return Ingest(
            package_id=mongo_dict["package_id"],
            s3_path=mongo_dict["s3_path"],
            s3_bucket_name=mongo_dict["s3_bucket_name"],
            admin_metadata=mongo_dict["admin_metadata"],
            status=IngestStatus[mongo_dict["status"]],
            depositing_application=DepositingApplication[mongo_dict["depositing_application"]]
        )
