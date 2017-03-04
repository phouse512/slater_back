### Admin Scripts

These are the scripts used to administer slater.


#### close_poll

this script is responsible for distributing coins out once a poll is closed. the two inputs
are the poll id and the correct answer id. it requires you to approve of them before it occurs.
also you need to close the poll by setting the `finished` flag to true before running this.

Example usage:
```
python3 close_poll.py <poll_id> <correct_answer_id>
```