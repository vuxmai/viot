from testcontainers.core.container import inside_container  # type: ignore
from testcontainers.core.generic import DbContainer  # type: ignore  # noqa: F401
from testcontainers.postgres import PostgresContainer  # type: ignore
from testcontainers.redis import AsyncRedisContainer  # type: ignore

# Issue: https://github.com/testcontainers/testcontainers-python/issues/475


class FixedPostgresContainer(PostgresContainer):
    def _shares_network(self):
        host = self.get_docker_client().host()
        gateway_ip = self.get_docker_client().gateway_ip(self._container.id)  # type: ignore

        if gateway_ip == host:
            return True
        return False

    def get_container_host_ip(self) -> str:
        if inside_container():
            if self._shares_network():
                return self.get_docker_client().bridge_ip(self._container.id)  # type: ignore
            return self.get_docker_client().gateway_ip(self._container.id)  # type: ignore

        return super().get_container_host_ip()


class FixedAsyncRedisContainer(AsyncRedisContainer):
    def _shares_network(self):
        host = self.get_docker_client().host()
        gateway_ip = self.get_docker_client().gateway_ip(self._container.id)  # type: ignore

        if gateway_ip == host:
            return True
        return False

    def get_container_host_ip(self) -> str:
        if inside_container():
            if self._shares_network():
                return self.get_docker_client().bridge_ip(self._container.id)  # type: ignore
            return self.get_docker_client().gateway_ip(self._container.id)  # type: ignore

        return super().get_container_host_ip()
