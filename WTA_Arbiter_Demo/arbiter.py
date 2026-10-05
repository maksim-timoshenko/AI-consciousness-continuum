class Arbiter:
    def __init__(self, hysteresis=15, critical_vh=90):
        self.hysteresis = hysteresis
        self.critical_vh = critical_vh
        self.current_winner = None

    def decide(self, priorities):
        """
        priorities: dict вида {"V_h": 100, "V_e": 70, "V_s": 10}
        Возвращает: (имя_победителя, пояснение)
        """
        vh = priorities.get("V_h")
        if vh is None:
            raise ValueError("V_h отсутствует в priorities")

        # Безусловное прерывание
        if vh >= self.critical_vh:
            self.current_winner = "V_h"
            return "V_h", "БЕЗУСЛОВНОЕ ПРЕРЫВАНИЕ!"

        leader = max(priorities, key=priorities.get)

        if self.current_winner is None:
            self.current_winner = leader
            return leader, None

        # Проверяем гистерезис
        if priorities[leader] > priorities[self.current_winner] + self.hysteresis:
            self.current_winner = leader
            return leader, None

        # Лидер не меняется
        if leader == self.current_winner:
            return self.current_winner, None

        # Гистерезис удерживает текущего победителя
        diff = priorities[leader] - priorities[self.current_winner]
        explanation = (
            f"Гистерезис: {leader} не может перехватить управление "
            f"у {self.current_winner} (разница {diff} меньше {self.hysteresis})"
        )
        return self.current_winner, explanation
