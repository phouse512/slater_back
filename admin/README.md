### Admin Scripts

These are the scripts used to administer slater.


#### close_poll

this script is responsible for distributing coins out once a poll is closed. the two inputs
are the poll id and the correct answer id. it requires you to approve of them before it occurs.
also you need to close the poll by setting the `finished` flag to true before running this.

Example usage (run from `slater_back` root):
```
python3 -m admin <poll_id> <correct_answer_id>
```

#### add_poll

next up is a script to add a poll and its answers. This needs to creat its bank
account and a couple other cleanup tasks.

#### unit tests

to run the unit tests, run the following from the root directory of
`slater_back`:

```
python3 -m unittest
```
