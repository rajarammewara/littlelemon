from rest_framework.throttling import UserRateThrottle

class ThreeCallsPerMinute(UserRateThrottle):   
    scope = 'three'