import argparse
import pathlib

parser = argparse.ArgumentParser(
    prog="Splctl",
    description="Splunk Installation Automation Tool.",
)

parser.add_argument(
    "-u",
    "--user",
    dest="username",
    default="splunkfwd",
    type=str,
    help="Specify the least privilege user. Default: splunkfwd.",
)

parser.add_argument(
    "-g",
    "--group",
    dest="groupname",
    default="splunkfwd",
    type=str,
    help="Specify the least privilege user group. Default: splunkfwd.",
)

parser.add_argument(
    "-a",
    "--apps",
    nargs="*",
    type=pathlib.Path,
    help="List of apps (paths or names) to import. Example: -a app1 app2.",
)

parser.add_argument(
    "-m",
    "--method",
    default="online",
    choices=["online", "local", "url"],
    type=str,
    help="Download method: 'online' (download from web), 'local' (use provided tarball) or 'URL' (use provided URL). Default: online.",
)

parser.add_argument(
    "-t",
    "--tar",
    dest="archive_path",
    type=pathlib.Path,
    help="Path to the Splunk UF tar archive (Required if method is local).",
)

parser.add_argument(
    "--url",
    type=str,
    help="Specify URL (Required if method is url).",
)

parser.add_argument(
    "-s",
    "--start",
    dest="start_service",
    default="yes",
    type=str,
    choices=["yes", "no"],
    help="Start Splunk service after installation. Default: yes.",
)

parser.add_argument(
    "-d",
    "--directory",
    dest="install_dir",
    type=pathlib.Path,
    default="/opt",
    help="Specify Splunk target installation path. Default: /opt.",
)


def get_args():
    args = parser.parse_args()

    if args.method == "local":
        if not args.tar:
            parser.error("Method 'local' requires --tar path.")

    if args.method == "url":
        if not args.url:
            parser.error("Method 'url' requires an url.")

    return args
