from __future__ import annotations
import hashlib
from ccp_studio.contracts.carousel_engine import CarouselPreviewPack, CarouselRenderBatchContract, CarouselSlideRenderReceipt

class CarouselRenderService:
    def render_batch(self, contract: CarouselRenderBatchContract):
        receipts = []
        for idx in range(1, contract.slide_count + 1):
            sha = hashlib.sha256(f"{contract.render_batch_contract_id}:{idx}".encode()).hexdigest()
            receipts.append(CarouselSlideRenderReceipt(
                slide_index=idx,
                render_batch_contract_id=contract.render_batch_contract_id,
                output_uri=f"storage/carousel/{contract.carousel_variant_id}/slide_{idx}.png",
                output_sha256=sha,
            ))
        return receipts, CarouselPreviewPack(
            carousel_variant_id=contract.carousel_variant_id,
            slide_receipt_ids=[r.slide_render_receipt_id for r in receipts],
        )
