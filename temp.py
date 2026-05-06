import numpy as np

ks = np.arange(2, 101) # shape (99,)
ns = np.arange(100001) # shape (100001,)
# this is a (100001, 99) table of remainders
REMAINDER_TABLE = ns[:, None] % ks[None, :]

# binary entropy
def hb(p):
    p = np.clip(p, 1e-15, 1 - 1e-15)
    return -(p * np.log2(p) + (1 - p) * np.log2(1 - p))

def H(p):
    p = p[p > 0]
    return -np.sum(p * np.log2(p))

class GameState:
    def __init__(self):
        # Initialize P: P[k, r]
        self.P = np.zeros((101, 101))
        for k in range(2, 101):
            self.P[k, :k] = 1.0
        self.P /= self.P.sum()
        
        self.history = []

    def system_entropy(self):
        return H(self.P)

    # this method will re-calculate the probs, and calculate the informational gain.
    def get_expected_entropy(self, n):
        k = np.arange(101).reshape(-1, 1)
        r = np.arange(101).reshape(1, -1)
        
        with np.errstate(divide='ignore', invalid='ignore'):
            mask = (n % k) == r
            
        p_match = np.sum(self.P * mask)
        p_miss = 1.0 - p_match

        e_h = 0.0
        if p_match > 0:
            e_h += p_match * H((self.P * mask) / p_match)
        if p_miss > 0:
            e_h += p_miss * H((self.P * (~mask)) / p_miss)
        return e_h
  
    def update(self, n, is_match):
        """
        Updates P based on a known outcome. 
        is_match: Boolean (True if n % k == r, False otherwise)
        """
        self.history.append(self.P.copy())
        
        # Calculate remainders for all possible k
        # row index is k, value is the r that would satisfy the match
        rs = n % self.ks
        
        # Create a filter for the matrix
        # We only care about k >= 2, but 0 and 1 have 0.0 probability anyway
        if is_match:
            # Keep only the entries where P[k, r] matches n % k == r
            new_P = np.zeros_like(self.P)
            # Efficiently pick P[k, n%k] for all k
            new_P[self.ks, rs] = self.P[self.ks, rs]
            self.P = new_P
        else:
            # Zero out the entries where n % k == r
            self.P[self.ks, rs] = 0.0

        # Normalize the remaining probability mass
        total_p = self.P.sum()
        if total_p > 0:
            self.P /= total_p
        else:
            # This happens if an outcome is mathematically impossible 
            # given previous updates.
            pass    
    def rollback(self):
        if self.history:
            self.P = self.history.pop()