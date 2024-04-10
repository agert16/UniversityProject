import unittest
import re
from datetime import time
from modules.scheduler import is_room_available
from modules.classroom import check_room_capacity
from modules.scheduler import timeslots_overlap, parse_timeslot

class SchedulingTestCase(unittest.TestCase):
    def test_room_availability_success(self):
        """Test room is reported as available when it should be."""
        self.assertTrue(is_room_available("university_id_2", "room_id_1", "Saturday 09:00-10:30"))

    def test_room_availability_failure(self):
        """Test room is reported as not available when it should not be."""
        self.assertTrue(is_room_available("university_id_2", "room_id_1", "Monday 09:00-10:30"))

    def test_sufficient_room_capacity(self):
        """Test that scheduling a class is successful when the expected number of attendees does not exceed room capacity."""
        self.assertTrue(check_room_capacity("university_id_2", "room_id_1", 40))

    def test_insufficient_room_capacity(self):
        """Test that scheduling a class fails when the expected number of attendees exceeds room capacity."""
        self.assertFalse(check_room_capacity("university_id_2", "room_id_1", 200))

class TestTimeslotOverlap(unittest.TestCase):
    def test_non_overlapping_same_day(self):
        timeslot1 = "Monday 09:00-10:00"
        timeslot2 = "Monday 10:00-11:00"
        self.assertFalse(timeslots_overlap(timeslot1, timeslot2), "Timeslots should not overlap")

    def test_overlapping_same_day(self):
        timeslot1 = "Monday 09:00-10:00"
        timeslot2 = "Monday 09:30-10:30"
        self.assertTrue(timeslots_overlap(timeslot1, timeslot2), "Timeslots should overlap")

    def test_different_days(self):
        timeslot1 = "Monday 09:00-10:00"
        timeslot2 = "Tuesday 09:00-10:00"
        self.assertFalse(timeslots_overlap(timeslot1, timeslot2), "Timeslots on different days should not overlap")

    def test_boundary_non_overlapping(self):
        timeslot1 = "Monday 09:00-10:00"
        timeslot2 = "Monday 10:00-11:00"
        self.assertFalse(timeslots_overlap(timeslot1, timeslot2), "Timeslots ending and starting at the same time should not overlap")

    def test_exact_overlap(self):
        timeslot1 = "Monday 09:00-10:00"
        timeslot2 = "Monday 09:00-10:00"
        self.assertTrue(timeslots_overlap(timeslot1, timeslot2), "Identical timeslots should overlap")

class TestParseTimeslot(unittest.TestCase):
    def test_valid_timeslot_parsing(self):
        # Test case for a valid timeslot
        test_cases = [
            ("Monday 09:00-10:00", ("Monday", time(9, 0), time(10, 0))),
            ("Tuesday 23:00-00:30", ("Tuesday", time(23, 0), time(0, 30))),
        ]
        for timeslot, expected in test_cases:
            with self.subTest(timeslot=timeslot):
                day, start, end = parse_timeslot(timeslot)
                self.assertEqual(day, expected[0], "Day should match")
                self.assertEqual(start, expected[1], "Start time should match")
                self.assertEqual(end, expected[2], "End time should match")
    
    def test_invalid_timeslot_format(self):
        # Test case for an invalid timeslot format
        invalid_timeslots = [
            "Monday 9:00-10:00",  # Missing leading zero
            "InvalidDay 12:00-25:00",  # Invalid day
        ]
        for timeslot in invalid_timeslots:
            with self.subTest(timeslot=timeslot):
                with self.assertRaises(ValueError):
                    parse_timeslot(timeslot)
    
    def test_end_time_before_start_time(self):
        # This tests if the end time before the start time correctly adjusts to the next day
        timeslot = "Monday 23:00-01:00"
        day, start, end = parse_timeslot(timeslot)
        self.assertTrue(end < start, "End time should be adjusted to next day")
        self.assertEqual(day, "Monday", "Day should be Monday")
        self.assertEqual(start, time(23, 0), "Start time should be 23:00")
        self.assertEqual(end, time(1, 0), "End time should be 01:00 (next day)")

if __name__ == '__main__':
    unittest.main()
