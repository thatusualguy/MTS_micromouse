import config
from config import FWD_WAIT_TIME
from motors import pwm
from sensors import get_encoders


def forward(dist_cells):

    # zero encoders
    get_encoders()

    sum_encoders = 0
    final_encoders = dist_cells * config.ONE_CELL_ENCODER

    while abs(final_encoders - sum_encoders  ) > config.FWD_ALLOWED_ERROR:
        pwm(100, FWD_WAIT_TIME, 100, FWD_WAIT_TIME)

