import logging
from typing import Optional

from pymongo.errors import PyMongoError
from tenacity import retry, stop_after_attempt, retry_if_exception_type, before_log

from app.common.infrastructure.data.mongo_interactor import MongoInteractor
from app.ingest.domain.models.ingest.depositing_application import DepositingApplication
from app.ingest.domain.models.ingest.ingest import Ingest
from app.ingest.domain.models.ingest.ingest_status import IngestStatus
from app.ingest.domain.repositories.exceptions.ingest_query_exception import IngestQueryException
from app.ingest.domain.repositories.exceptions.ingest_save_exception import IngestSaveException
from app.ingest.domain.repositories.ingest_repository import IIngestRepository


class IngestRepository(IIngestRepository, MongoInteractor):

    @retry(
        stop=stop_after_attempt(MongoInteractor._MONGO_OPERATION_MAX_RETRIES),
        retry=retry_if_exception_type(IngestSaveException),
        reraise=True,
        before=before_log(logging.getLogger(), logging.INFO)
    )
    def save(self, ingest: Ingest) -> None:
        try:
            self._logger.info("Saving ingest with package id " + ingest.package_id + " to MongoDB...")
            db = self._get_database()
            db.ingests.replace_one(
                {"package_id": ingest.package_id},
                self.__transform_ingest_to_mongo_dict(ingest),
                upsert=True
            )
            self._logger.info("Ingest with package id " + ingest.package_id + " saved")
        except PyMongoError as pme:
            self._logger.error(str(pme))
            raise IngestSaveException(ingest.package_id, str(pme))

    @retry(
        stop=stop_after_attempt(MongoInteractor._MONGO_OPERATION_MAX_RETRIES),
        retry=retry_if_exception_type(IngestQueryException),
        reraise=True,
        before=before_log(logging.getLogger(), logging.INFO)
    )
    def get_by_package_id(self, package_id: str) -> Optional[Ingest]:
        try:
            self._logger.info("Getting ingest with package id " + package_id + " from MongoDB...")
            db = self._get_database()
            ingest_mongo_dict = db.ingests.find_one({"package_id": package_id})
            if ingest_mongo_dict is None:
                self._logger.info("Ingest with package id " + package_id + " not found")
                return None
            self._logger.info("Ingest with package id " + package_id + " found")
            return self.__transform_mongo_dict_to_ingest(ingest_mongo_dict)
        except PyMongoError as pme:
            self._logger.error(str(pme))
            raise IngestQueryException(package_id, str(pme))

    def __transform_ingest_to_mongo_dict(self, ingest: Ingest) -> dict:
        return {
            "package_id": ingest.package_id,
            "s3_path": ingest.s3_path,
            "s3_bucket_name": ingest.s3_bucket_name,
            "admin_metadata": ingest.admin_metadata,
            "status": ingest.status.value,
            "depositing_application": ingest.depositing_application.value,
            "drs_url": ingest.drs_url
        }

    def __transform_mongo_dict_to_ingest(self, mongo_dict: dict) -> Ingest:
        return Ingest(
            package_id=mongo_dict["package_id"],
            s3_path=mongo_dict["s3_path"],
            s3_bucket_name=mongo_dict["s3_bucket_name"],
            admin_metadata=mongo_dict["admin_metadata"],
            status=IngestStatus[mongo_dict["status"]],
            depositing_application=DepositingApplication[mongo_dict["depositing_application"]],
            drs_url=mongo_dict.get("drs_url", None)
        )
