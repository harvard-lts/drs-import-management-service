from typing import Tuple, Dict


class IngestPostController:

    def __call__(self) -> Tuple[Dict, int]:
        return {"data": {"ingest_status": "processing_ingest"}}, 202
