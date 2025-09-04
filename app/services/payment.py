# Заглушка платежного сервиса


class PaymentService:
    def create_invoice(self, amount: int, description: str) -> str:
        raise NotImplementedError