import io
import logging
from pathlib import Path

import click
from rdvc.slurm.ssh_client import SSHClient

log = logging.getLogger("rdvc")


def submit_remote(client: SSHClient, sbatch_script: str, rdvc_dir: str = "~/.rdvc") -> None:
    """Submit an sbatch script to the remote SLURM cluster.
    
    Args:
        client: SSH client connection to remote host
        sbatch_script: The sbatch script content to submit
        rdvc_dir: Path to the rdvc directory on the remote host (default: ~/.rdvc)
    """
    submissions_dir = Path(rdvc_dir) / "submissions"
    sbatch_script_fo = io.BytesIO(sbatch_script.encode("utf-8"))
    temp_sbatch_path = client.make_tmpdir("rdvc-sbatch-XXXXXXXXXX")

    log.info(f"Copying sbatch submission file to {temp_sbatch_path}.")
    client.upload(sbatch_script_fo, temp_sbatch_path, chmod=775)

    job_id = client.submit_sbatch(temp_sbatch_path)
    click.echo(f"Submitted batch job {job_id}.")

    final_remote_file_path = submissions_dir / f"{job_id}.sbatch.sh"
    client.move(temp_sbatch_path, str(final_remote_file_path))
