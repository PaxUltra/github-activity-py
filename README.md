![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/PaxUltra/github-activity-py/ci.yml)

# github-activity-py
Simple Python CLI tool to fetch GitHub user activity using the GitHub REST API.

## Requirements
- Python 3.6+

## Installation

1. Clone the repository wherever you want it to live
```bash
git clone https://github.com/PaxUltra/github-activity-py.git
```
2. Change directory into the `github-activity-py` directory
```bash
cd github-activity-py
```
## Usage

The script works via passing command line arguments to the `github_activity.py` file.

```bash
python github_activity.py <username>
```
Output is printed directly to the terminal.

### Errors

The GitHub API will return a `404` error if you try to access a resource that does not exist, or is forbidden somehow.

Errors `403` and `429` are returned if you exceed the rate limit.

Full documentation for the GitHub REST API can be found [here](https://docs.github.com/en/rest/using-the-rest-api).

### Testing

To run the provided tests, execute:
```bash
python -m unittest test_github_activity.py
```

This project was built for the [GitHub User Activity](https://roadmap.sh/projects/github-user-activity) project on roadmap.sh.
