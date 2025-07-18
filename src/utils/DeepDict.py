class DeepDict(dict):
    def copy(self):
        return {k: v.copy() if (hasattr(v, 'copy') and callable(getattr(v, 'copy')))
            else v for k, v in self.items()}