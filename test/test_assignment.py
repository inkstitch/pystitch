import unittest

from pystitch.Assignment import minimal_assignment


def assign(costs):
    """Calls minimal_assignment with {worker: {job: cost}} and returns {worker: job}."""
    workers = list(costs)
    jobs = list(costs[workers[0]])
    matrix = [[costs[worker][job] for job in jobs] for worker in workers]
    columns = minimal_assignment(matrix)
    return {worker: jobs[column] for worker, column in zip(workers, columns)}


class TestAssignment(unittest.TestCase):
    """The algorithm is generic (unrelated to rest of pystitch), so keeping the tests generic too"""

    def test_wikipedia_example(self):
        # https://en.wikipedia.org/wiki/Hungarian_algorithm#Example
        # Greedy would assign Bob his cheapest job (floors, 2) and end up at 18.
        result = assign({
            "Alice": {"bathroom": 8, "floors": 4, "windows": 7},
            "Bob":   {"bathroom": 5, "floors": 2, "windows": 3},
            "Carol": {"bathroom": 9, "floors": 4, "windows": 8},
        })
        # Results in the cheapest combination: 8 + 3 + 4 = 15
        self.assertEqual(result, {
            "Alice": "bathroom",
            "Bob": "windows",
            "Carol": "floors",
        })

    def test_more_jobs_than_workers(self):
        result = assign({
            "Alice": {"bathroom": 8, "floors": 4, "windows": 7, "dishes": 1},
            "Bob":   {"bathroom": 5, "floors": 2, "windows": 3, "dishes": 6},
            "Carol": {"bathroom": 9, "floors": 4, "windows": 8, "dishes": 7},
        })
        self.assertEqual(result, {
            "Alice": "dishes",
            "Bob": "windows",
            "Carol": "floors",
        })

    def test_single_worker_takes_cheapest_job(self):
        result = assign({
            "Alice": {"bathroom": 8, "floors": 4, "windows": 7},
        })
        self.assertEqual(result, {"Alice": "floors"})

    def test_identical_cost_goes_to_worker_who_saves_most(self):
        result = assign({
            "Alice": {"bathroom": 2, "floors": 1},
            "Bob":   {"bathroom": 9, "floors": 1},
        })
        self.assertEqual(result, {"Alice": "bathroom", "Bob": "floors"})


if __name__ == "__main__":
    unittest.main()
