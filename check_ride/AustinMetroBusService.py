from CheckRideService import CheckRideService
from google.transit import gtfs_realtime_pb2
import time
import boto3
from helper.AustinMetroBusStopNames import AustinMetroBusStopNames


class AustinMetroBusService(CheckRideService):

    def check_ride(self, route, stop, agency):
        s3 = boto3.resource('s3')
        s3_object = s3.Object('austin-transit', 'tripupdates.pb')

        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(s3_object.get()['Body'].read())

        stop_time_updates_raw = list(
            map(lambda x: list(x.trip_update.stop_time_update),
                filter(lambda x: x.trip_update.trip.route_id == route, feed.entity)))

        if len(stop_time_updates_raw) == 0:
            return [], None

        stop_time_updates = filter(lambda x: x.stop_id == stop, reduce(list.__add__, stop_time_updates_raw))

        if len(stop_time_updates) == 0:
            return [], None

        current_time = time.time()

        minutes_list = []

        for stu in stop_time_updates:
            minutes = int((stu.arrival.time - current_time) / 60)
            if minutes >= 0:
                minutes_list.append(minutes)

        return sorted(minutes_list)[:2], AustinMetroBusStopNames.get_stop_name(stop)


if __name__ == '__main__':
    print AustinMetroBusService().check_ride('481', '490', 'austin-metro-bus')
