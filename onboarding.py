import os
import re
import argparse
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
                 security=False,
                 base_output_dir="output"):

        self.user = user
        self.crq = crq
        self.app_code = app_code
        self.env = env.lower()
        self.add_info = add_info
        self.retention = retention
        self.syslog = syslog
        self.port = port
        self.security = security
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
            raise ValueError(f"Invalid retention. Choose from: {list(self.RETENTION_MAP.keys())}")
        if self.syslog and not self.port:
            raise ValueError("Port required when --syslog is used")

    # -----------------------------
    # Helpers
    # -----------------------------
    def _build_index_name(self):
        base = f"appl_{self.app_code}_{self.env}_{self.add_info}"
        if self.security:
            return f"{base}-sec"
        return base

    def _build_header(self):
        return f"# {self.app_code.upper()} {self.env.upper()} {self.crq} {self.initials} {self.date_str}"

    def _get_retention_seconds(self):
        return self.RETENTION_MAP[self.retention]

    def _get_index_size(self):
        if self.security or self.env == "prod":
            return "4294967296"
        return "720GB"

    def _get_input_path(self):
        return f"udp://{self.port}" if self.syslog else "monitor://"

    # -----------------------------
    # Config Generators
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

    def generate_authentication(self):
        return f"""{self.header}
{self.index_name} = sec-splunk-appl-{self.app_code}-{self.env}-{self.add_info}
"""

    # -----------------------------
    # Print Output
    # -----------------------------
    def print_all(self):
        print("\n===== INDEXES.CONF =====")
        print(self.generate_index_conf())

        print("\n===== INPUTS.CONF =====")
        print(self.generate_inputs_conf())

        print("\n===== SERVERCLASS.CONF =====")
        print(self.generate_serverclass())

        print("\n===== AUTHORIZE.CONF =====")
        print(self.generate_authorize())

        print("\n===== AUTHENTICATION.CONF =====")
        print(self.generate_authentication())

    # -----------------------------
    # Write to single CRQ file
    # -----------------------------
    def write_to_single_file(self):
        os.makedirs(self.base_output_dir, exist_ok=True)
        file_path = os.path.join(self.base_output_dir, f"{self.crq}.txt")

        content = f"""===== INDEXES.CONF =====
{self.generate_index_conf()}

===== INPUTS.CONF =====
{self.generate_inputs_conf()}

===== SERVERCLASS.CONF =====
{self.generate_serverclass()}

===== AUTHORIZE.CONF =====
{self.generate_authorize()}

===== AUTHENTICATION.CONF =====
{self.generate_authentication()}
"""

        with open(file_path, "w") as f:
            f.write(content.strip())

        return file_path


# -----------------------------
# CLI Argument Parsing
# -----------------------------
def parse_args():
    parser = argparse.ArgumentParser(description="Splunk Onboarding Generator")

    parser.add_argument("--user", required=True, help="Username")
    parser.add_argument("--crq", required=True, help="CRQ number (CRQ + 12 digits)")
    parser.add_argument("--app", required=True, help="Application code")
    parser.add_argument("--env", required=True, help="Environment (dev/prod/etc)")
    parser.add_argument("--info", required=True, help="Additional info")
    parser.add_argument("--retention", required=True, help="Retention (e.g., 3M, 1Y)")
    parser.add_argument("--syslog", action="store_true", help="Enable syslog input")
    parser.add_argument("--port", type=int, help="Port (required if syslog enabled)")
    parser.add_argument("--security", action="store_true", help="Mark index as security (adds -sec suffix)")
    parser.add_argument("--output", default="output", help="Output directory")

    return parser.parse_args()


# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    args = parse_args()

    onboarding = SplunkOnboarding(
        user=args.user,
        crq=args.crq,
        app_code=args.app,
        env=args.env,
        add_info=args.info,
        retention=args.retention,
        syslog=args.syslog,
        port=args.port,
        security=args.security,
        base_output_dir=args.output
    )

    # Print configs to console
    onboarding.print_all()

    # Write all configs to single CRQ text file
    file_path = onboarding.write_to_single_file()
    print(f"\nOutput written to: {file_path}")
