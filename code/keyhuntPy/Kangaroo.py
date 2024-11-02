from hashlib import sha256

from code.keyhuntPy.kangaroo import scalar_mult, P


class PollardKangaroo:
    def __init__(self, curve_order, generator_point, max_steps=1000):
        self.curve_order = curve_order  # Order of the elliptic curve group
        self.generator = generator_point
        self.max_steps = max_steps  # Limit number of steps for testing

    def random_step(self, point):
        """
        Defines a small, fixed random step based on a hash of the point coordinates.
        This approach generates a pseudorandom 'jump' for the kangaroo within a limited set.
        """
        point_str = f"{point.x}{point.y}".encode()
        step = int(sha256(point_str).hexdigest(), 16) % 10 + 1  # Limit steps to a small range [1, 10]
        return step

    def tame_kangaroo(self, start_point, target_value):
        """
        The tame kangaroo moves from a known start position up to a target value.
        """
        current_point = start_point
        accumulated_steps = 0

        for _ in range(self.max_steps):  # Limit number of steps
            step_size = self.random_step(current_point)
            accumulated_steps += step_size
            current_point = scalar_mult(step_size, self.generator, P)

            # Store position and steps to detect collisions with wild kangaroo
            if current_point in self.tame_positions:
                break
            self.tame_positions[current_point] = accumulated_steps

            # Break if reached or exceeded target value
            if accumulated_steps >= target_value:
                break

        return current_point, accumulated_steps

    def wild_kangaroo(self, start_point):
        """
        The wild kangaroo jumps randomly, hoping to meet with the tame.
        """
        current_point = start_point
        accumulated_steps = 0

        for _ in range(self.max_steps):  # Limit number of steps
            step_size = self.random_step(current_point)
            accumulated_steps += step_size
            current_point = scalar_mult(step_size, self.generator, P)

            # Check for collision with tame kangaroo positions
            if current_point in self.tame_positions:
                return accumulated_steps + self.tame_positions[current_point]  # Return combined steps as result

        return None  # Return None if no collision detected
