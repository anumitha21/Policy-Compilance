# guardrails/policy_guard.py

class PolicyGuard:
    def __init__(self, valid_policies: list[str]):
        """
        valid_policies: list of policy titles allowed
        """
        self.valid_policies = set(valid_policies)

    def filter_output(self, output_text: str, citations: list[str]) -> dict:
        """
        Checks if citations in output are valid.
        Returns:
            {
                "is_valid": bool,
                "invalid_citations": list[str]
            }
        """
        invalid = [c for c in citations if any(policy not in self.valid_policies for policy in c)]
        return {
            "is_valid": len(invalid) == 0,
            "invalid_citations": invalid
        }
