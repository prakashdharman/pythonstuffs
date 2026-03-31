import os
import re
from datetime import datetime


class SplunkOnboarding:

    RETENTION_MAP = {
        "2W": 1209600,
        "1M": 2592000,
        "2M": 5184000,
        "3M": 7776000,
        "6M": 15552000,
        "1Y": 31536000,
        "2Y": 63072000,
        "3Y": 94608000,
        "4Y": 126144000,
        "5Y": 157680000
    }

    def __init__(self, user, crq, app_code, env, add_info,
                 retention, syslog=False, port=None,
                 base_output_dir="output"):

        self.user = user
        self.crq = crq
        self.app_code = app_code
        self.env = env.lower()
        self.add_info = add_info
        self.retention = retention
        self.syslog = syslog
        self.port = port
        self.base_output_dir = base_output_dir

        self.validate_inputs()

        self.index_name = self._build_index_name()
        self.app_name = f"company_intg_{self.index_name}"

        self.retention_secs = self._get_retention_seconds()
        self.index_size = self._get_index_size()

        self.date_str = datetime.now().strftime("%Y%m%d")
        self.initials = self.user[:3].upper()
        self.header = self._build_header()

    # -----------------------------
    # Validation
    # -----------------------------
    def validate_inputs(self):
        if not re.match(r"^CRQ\d{12}$", self.crq):
            raise ValueError("CRQ must be 'CRQ' followed by 12 digits")

        if self.retention not in self.RETENTION_MAP:
            raise ValueError("Invalid retention value")

        if self.syslog and not self.port:
            raise ValueError("Port required for syslog")

    # -----------------------------
    # Internal helpers
    # -----------------------------
    def _build_index_name(self):
        return f"appl_{self.app_code}_{self.env}_{self.add_info}"

    def _build_header(self):
        return f"# {self.app_code.upper()} {self.env.upper()} {self.crq} {self.initials} {self.date_str}"

    def _get_retention_seconds(self):
        return self.RETENTION_MAP[self.retention]

    def _get_index_size(self):
        if self.index_name.endswith("-sec") or self.env == "prod":
            return "4294967296"
        return "720GB"

    def _get_input_path(self):
        return f"udp://{self.port}" if self.syslog else "monitor://"

    # -----------------------------
    # Config generators
    # -----------------------------
    def generate_index_conf(self):
        return f"""{self.header}
#################################################
[{self.index_name}]
homePath = volume:preprodenv_hot/{self.index_name}/db
coldPath = volume:preprodenv_cold/{self.index_name}/colddb
thawedPath = /splunk/coldindex/thawed/{self.index_name}/thaweddb
frozenTimePeriodInSecs = {self.retention_secs}
maxTotalDataSizeMB = {self.index_size}
"""

    def generate_inputs_conf(self):
        return f"""{self.header}
[{self._get_input_path()}]
index = {self.index_name}
sourcetype =
"""

    def generate_serverclass(self):
        return f"""{self.header}
###################*############################*####*#

[serverClass: {self.app_name}]
whitelist.0 =

[serverClass: {self.app_name}:app:{self.app_name}]
"""

    def generate_authorize(self):
        return f"""{self.header}
###################*############################*####*#
importRoles = user
srchIndexesAllowed = {self.index_name}
srchIndexesDefault = {self.index_name}
srchFilter = index::{self.index_name}
"""

    def generate_meta(self):
        return f"""[]
access = read : [ * ], write : [ admin ]
export = system
"""

    # -----------------------------
    # File writer
    # -----------------------------
    def create_app_structure(self):
        app_root = os.path.join(self.base_output_dir, self.app_name)

        paths = {
            "local": os.path.join(app_root, "local"),
            "default": os.path.join(app_root, "default"),
            "metadata": os.path.join(app_root, "metadata"),
        }

        # Create directories
        for path in paths.values():
            os.makedirs(path, exist_ok=True)

        # Write files
        files = {
            os.path.join(paths["default"], "indexes.conf"): self.generate_index_conf(),
            os.path.join(paths["local"], "inputs.conf"): self.generate_inputs_conf(),
            os.path.join(paths["default"], "serverclass.conf"): self.generate_serverclass(),
            os.path.join(paths["default"], "authorize.conf"): self.generate_authorize(),
            os.path.join(paths["metadata"], "local.meta"): self.generate_meta(),
        }

        for filepath, content in files.items():
            with open(filepath, "w") as f:
                f.write(content)

        return app_root
        
    def generate_authentication(self):
        return f"""{self.header}
        {self.index_name} = sec-splunk-appl-{self.app_code}-{self.env}-{self.add_info}
        """ 

    def print_all(self):
        print("\n===== INDEXES.CONF =====")
        print(self.generate_index_conf())

        print("\n===== INPUTS.CONF =====")
        print(self.generate_inputs_conf())

        print("\n===== SERVERCLASS.CONF =====")
        print(self.generate_serverclass())

        print("\n===== AUTHORIZE.CONF =====")
        print(self.generate_authorize())

        print("\n===== METADATA (local.meta) =====")
        print(self.generate_meta())


# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":

    onboarding = SplunkOnboarding(
        user="john",
        crq="CRQ123456789012",
        app_code="billing",
        env="prod",
        add_info="sec",
        retention="3M",
        syslog=True,
        port=514
    )

    onboarding.print_all()
    path = onboarding.create_app_structure()
    print(f"\nApp created at: {path}")
