import pytest
import struct

from common.package import NetworkPackageBuilder, ActionType, CommandType, ErrorType, PackageType, RequestType


class TestPackageBuilder:

    def test_request(self):
        builder = NetworkPackageBuilder()
        builder.set_package(PackageType.REQUEST)
        builder.set_action(RequestType.GAME_STATE)
        package = builder.build()
        assert package == bytes([PackageType.REQUEST.value, RequestType.GAME_STATE.value, 0])

    def test_command(self):
        builder = NetworkPackageBuilder()
        builder.set_package(PackageType.ACTION)
        builder.set_action(ActionType.MOVE)
        format = "!ffBB"
        builder.set_data(format, 15.5, 12.3, True, 3)
        package = builder.build()
        assert package == (bytes(
            [PackageType.ACTION.value, ActionType.MOVE.value, struct.calcsize(format)]
            ) + b'Ax\x00\x00AD\xcc\xcd\x01\x03')

    def test_raise(self):
        with pytest.raises(struct.error):
            builder = NetworkPackageBuilder()
            builder.set_package(PackageType.ACTION)
            builder.set_action(ActionType.MOVE)
            format = "!ffBB"
            builder.set_data(format, 15.5, 12.3, True, 10**3)
            builder.build()