class NoHashingHasher():
    """
    A hasher that aims to show the password as plain text in the database.
    """

    algorithm = "nohashing"
    iterations = 0
    # digest = hashlib.sha256

    def encode(self, password, salt, iterations=None):
        # self._check_encode_args(password, salt)
        iterations = iterations or self.iterations
        # salt = force_str(salt)
        salt = "none"
        # hash = pbkdf2(password, salt, iterations, digest=self.digest)
        # hash = base64.b64encode(hash).decode("ascii").strip()
        hash = password
        return "%s$%d$%s$%s" % (self.algorithm, iterations, salt, hash)

    def salt(self):
        return None

    def decode(self, encoded):
        algorithm, iterations, salt, hash = encoded.split("$", 3)
        assert algorithm == self.algorithm
        return {
            "algorithm": algorithm,
            "hash": hash,
            "iterations": int(iterations),
            "salt": salt,
        }

    def verify(self, password, encoded):
        decoded = self.decode(encoded)
        encoded_2 = self.encode(password, decoded["salt"], decoded["iterations"])
        # return constant_time_compare(encoded, encoded_2)
        return encoded == encoded_2

    def safe_summary(self, encoded):
        decoded = self.decode(encoded)
        return {
            ("algorithm"): decoded["algorithm"],
            ("iterations"): decoded["iterations"],
            ("salt"): (decoded["salt"]),
            ("hash"): (decoded["hash"]),
        }

    def must_update(self, encoded):
        return
        decoded = self.decode(encoded)
        update_salt = must_update_salt(decoded["salt"], self.salt_entropy)
        return (decoded["iterations"] != self.iterations) or update_salt

    def harden_runtime(self, password, encoded):
        return
        decoded = self.decode(encoded)
        extra_iterations = self.iterations - decoded["iterations"]
        if extra_iterations > 0:
            self.encode(password, decoded["salt"], extra_iterations)
