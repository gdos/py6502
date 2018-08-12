#!/usr/bin/env python
# pylint: disable=too-many-lines

"""6502 assembly."""

__author__ = 'Radoslaw Matusiak'
__copyright__ = 'Copyright (c) 2018 Radoslaw Matusiak'
__license__ = 'MIT'


from enum import Enum

from mos6502.helpers import to_signed_byte


class AddressMode(Enum):
    """Address modes enum."""

    ACCUMULATOR = 1
    ABSOLUTE = 2
    ABSOLUTE_X_INDEXED = 3
    ABSOLUTE_Y_INDEXED = 4
    IMMEDIATE = 5
    IMPLIED = 6
    INDIRECT = 7
    INDEXED_X_INDIRECT = 8
    INDIRECT_Y_INDEXED = 9
    RELATIVE = 10
    ZEROPAGE = 11
    ZEROPAGE_X_INDEXED = 12
    ZEROPAGE_Y_INDEXED = 13

    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    @staticmethod
    def calculate_operand(mode, bytez, mcu, memory):
        """
        Calculate instruction operand based on address mode.

        :param mode: Address mode.
        :param bytez: Raw operation bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Calculated operation operand.
        """
        address = None
        operand = None

        if mode == AddressMode.ACCUMULATOR:
            operand = mcu.a.value
        elif mode == AddressMode.ABSOLUTE:
            assert len(bytez) == 2, 'Invalid bytes length for Absolute address mode.'
            address = bytez[1] << 8 | bytez[0]
            operand = memory[address]
        elif mode == AddressMode.ABSOLUTE_X_INDEXED:
            assert len(bytez) == 2, 'Invalid bytes length for Absolute X indexed address mode.'
            address = bytez[1] << 8 | bytez[0]
            address += mcu.x.value
            operand = memory[address]
        elif mode == AddressMode.ABSOLUTE_Y_INDEXED:
            assert len(bytez) == 2, 'Invalid bytes length for Absolute Y indexed address mode.'
            address = bytez[1] << 8 | bytez[0]
            address += mcu.y.value
            operand = memory[address]
        elif mode == AddressMode.IMMEDIATE:
            assert len(bytez) == 1, 'Invalid bytes length for Immediate address mode.'
            operand = bytez[0]
        elif mode == AddressMode.IMPLIED:
            pass  # Operand implied
        elif mode == AddressMode.INDIRECT:
            assert len(bytez) == 2, 'Invalid bytes length for Indirect address mode.'
            address = bytez[1] << 8 | bytez[0]
            operand = memory[address]
        elif mode == AddressMode.INDEXED_X_INDIRECT:
            assert len(bytez) == 1, 'Invalid bytes length for Indexed Indirect address mode.'
            address = (bytez[0] + mcu.x.value) & 0xff
            operand = memory[address] + (memory[address + 1] << 8)
        elif mode == AddressMode.INDIRECT_Y_INDEXED:
            assert len(bytez) == 1, 'Invalid bytes length for Indirect Indexed address mode.'
            address = (bytez[0] + mcu.y.value) & 0xff
            operand = memory[address] + (memory[address + 1] << 8)
        elif mode == AddressMode.RELATIVE:
            assert len(bytez) == 1, 'Invalid bytes length for Relative address mode.'
            operand = to_signed_byte(bytez[0]) + mcu.pc.value
        elif mode == AddressMode.ZEROPAGE:
            assert len(bytez) == 1, 'Invalid bytes length for Zeropage address mode.'
            address = bytez[0]
            operand = memory[address]
        elif mode == AddressMode.ZEROPAGE_X_INDEXED:
            assert len(bytez) == 1, 'Invalid bytes length for Zeropage X indexed address mode.'
            address = (bytez[0] + mcu.x.value) & 0xff
            operand = memory[address]
        elif mode == AddressMode.ZEROPAGE_Y_INDEXED:
            assert len(bytez) == 1, 'Invalid bytes length for Zeropage Y indexed address mode.'
            address = (bytez[0] + mcu.y.value) & 0xff
            operand = memory[address]
        else:
            assert False, 'Invalid mode!'

        return operand, address


class Instruction(object):  # pylint: disable=too-few-public-methods
    """Base class for assembly instructions."""
    pass


class ADC(Instruction):  # pylint: disable=too-few-public-methods
    """Add Memory to Accumulator with Carry"""

    MNEMONIC = 'ADC'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0x69: (AddressMode.IMMEDIATE, 2, 2, 0),
        0x65: (AddressMode.ZEROPAGE, 2, 3, 0),
        0x75: (AddressMode.ZEROPAGE_X_INDEXED, 2, 4, 0),
        0x6D: (AddressMode.ABSOLUTE, 3, 4, 0),
        0x7D: (AddressMode.ABSOLUTE_X_INDEXED, 3, 4, 1),
        0x79: (AddressMode.ABSOLUTE_Y_INDEXED, 3, 4, 1),
        0x61: (AddressMode.INDEXED_X_INDIRECT, 2, 6, 0),
        0x71: (AddressMode.INDIRECT_Y_INDEXED, 2, 5, 1)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        mode, _, _, _ = ADC.INSTRUCTIONS[opcode]
        operand, _ = AddressMode.calculate_operand(mode, bytez, mcu, memory)

        val = mcu.a.signed + operand + mcu.sr.C

        mcu.a.value = val

        mcu.sr.set_flags(val, 'NZCV')


class AND(Instruction):  # pylint: disable=too-few-public-methods
    """AND Memory with Accumulator"""

    MNEMONIC = 'AND'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0x29: (AddressMode.IMMEDIATE, 2, 2, 0),
        0x25: (AddressMode.ZEROPAGE, 2, 3, 0),
        0x35: (AddressMode.ZEROPAGE_X_INDEXED, 2, 4, 0),
        0x2D: (AddressMode.ABSOLUTE, 3, 4, 0),
        0x3D: (AddressMode.ABSOLUTE_X_INDEXED, 3, 4, 1),
        0x39: (AddressMode.ABSOLUTE_Y_INDEXED, 3, 4, 1),
        0x21: (AddressMode.INDEXED_X_INDIRECT, 2, 6, 0),
        0x31: (AddressMode.INDIRECT_Y_INDEXED, 2, 5, 1)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        mode, _, _, _ = AND.INSTRUCTIONS[opcode]
        operand, _ = AddressMode.calculate_operand(mode, bytez, mcu, memory)

        val = mcu.a.value & operand
        mcu.a.value = val

        mcu.sr.set_flags(val, 'NZ')


class ASL(Instruction):  # pylint: disable=too-few-public-methods
    """Shift Left One Bit (Memory or Accumulator)"""

    MNEMONIC = 'ASL'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0x0A: (AddressMode.ACCUMULATOR, 1, 2, 0),
        0x06: (AddressMode.ZEROPAGE, 2, 5, 0),
        0x16: (AddressMode.ZEROPAGE_X_INDEXED, 2, 6, 0),
        0x0E: (AddressMode.ABSOLUTE, 3, 6, 0),
        0x1E: (AddressMode.ABSOLUTE_X_INDEXED, 3, 7, 0)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        mode, _, _, _ = ASL.INSTRUCTIONS[opcode]
        operand, _ = AddressMode.calculate_operand(mode, bytez, mcu, memory)

        val = mcu.a.value << operand
        mcu.a.value = val

        mcu.sr.set_flags(val, 'NZC')


class BCC(Instruction):  # pylint: disable=too-few-public-methods
    """Branch on Carry Clear"""

    MNEMONIC = 'BCC'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0x90: (AddressMode.RELATIVE, 2, 3, 1)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        mode, _, _, _ = BCC.INSTRUCTIONS[opcode]
        operand, _ = AddressMode.calculate_operand(mode, bytez, mcu, memory)

        if mcu.sr.C == 0:
            mcu.pc.value += operand


class BCS(Instruction):  # pylint: disable=too-few-public-methods
    """Branch on Carry Set"""

    MNEMONIC = 'BCS'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0xB0: (AddressMode.RELATIVE, 2, 3, 1)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        mode, _, _, _ = BCS.INSTRUCTIONS[opcode]
        operand, _ = AddressMode.calculate_operand(mode, bytez, mcu, memory)

        if mcu.sr.C == 0:
            mcu.pc.value += operand


class BEQ(Instruction):  # pylint: disable=too-few-public-methods
    """Branch on Carry Set"""

    MNEMONIC = 'BCS'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0xF0: (AddressMode.RELATIVE, 2, 3, 1)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        mode, _, _, _ = BEQ.INSTRUCTIONS[opcode]
        operand, _ = AddressMode.calculate_operand(mode, bytez, mcu, memory)

        if mcu.sr.Z == 1:
            mcu.pc.value += operand


class BIT(Instruction):  # pylint: disable=too-few-public-methods
    """Test Bits in Memory with Accumulator"""

    MNEMONIC = 'BIT'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0x24: (AddressMode.ZEROPAGE, 2, 3, 0),
        0x2C: (AddressMode.RELATIVE, 3, 4, 0)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        mode, _, _, _ = ASL.INSTRUCTIONS[opcode]
        operand, _ = AddressMode.calculate_operand(mode, bytez, mcu, memory)

        val = mcu.a.value << operand
        m7 = 1 if (val & (1 << 7)) > 0 else 0  # pylint: disable=invalid-name
        m6 = 1 if (val & (1 << 6)) > 0 else 0  # pylint: disable=invalid-name
        mcu.sr.N = m7
        mcu.sr.V = m6

        mcu.sr.set_flags(val, 'Z')


class BMI(Instruction):  # pylint: disable=too-few-public-methods
    """Branch on Result Minus"""

    MNEMONIC = 'BMI'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0x30: (AddressMode.RELATIVE, 2, 3, 1)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        mode, _, _, _ = BMI.INSTRUCTIONS[opcode]
        operand, _ = AddressMode.calculate_operand(mode, bytez, mcu, memory)

        if mcu.sr.N == 1:
            mcu.pc.value += operand


class BNE(Instruction):  # pylint: disable=too-few-public-methods
    """Branch on Result not Zero"""

    MNEMONIC = 'BNE'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0xD0: (AddressMode.RELATIVE, 2, 3, 1)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        mode, _, _, _ = BNE.INSTRUCTIONS[opcode]
        operand, _ = AddressMode.calculate_operand(mode, bytez, mcu, memory)

        if mcu.sr.Z == 0:
            mcu.pc.value += operand


class BPL(Instruction):  # pylint: disable=too-few-public-methods
    """Branch on Result Plus"""

    MNEMONIC = 'BPL'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0x10: (AddressMode.RELATIVE, 2, 3, 1)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        mode, _, _, _ = BPL.INSTRUCTIONS[opcode]
        operand, _ = AddressMode.calculate_operand(mode, bytez, mcu, memory)

        if mcu.sr.N == 0:
            mcu.pc.value += operand


class BRK(Instruction):  # pylint: disable=too-few-public-methods
    """Force Break"""

    MNEMONIC = 'BRK'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0x00: (AddressMode.IMPLIED, 1, 7, 0)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        pass


class BVC(Instruction):  # pylint: disable=too-few-public-methods
    """Branch on Overflow Clear"""

    MNEMONIC = 'BVC'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0x50: (AddressMode.RELATIVE, 2, 3, 1)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        mode, _, _, _ = BVC.INSTRUCTIONS[opcode]
        operand, _ = AddressMode.calculate_operand(mode, bytez, mcu, memory)

        if mcu.sr.V == 0:
            mcu.pc.value += operand


class BVS(Instruction):  # pylint: disable=too-few-public-methods
    """Branch on Overflow Set"""

    MNEMONIC = 'BVS'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0x70: (AddressMode.RELATIVE, 2, 3, 1)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        mode, _, _, _ = BVS.INSTRUCTIONS[opcode]
        operand, _ = AddressMode.calculate_operand(mode, bytez, mcu, memory)

        if mcu.sr.V == 1:
            mcu.pc.value += operand


class CLC(Instruction):  # pylint: disable=too-few-public-methods
    """Clear Carry Flag"""

    MNEMONIC = 'CLC'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0x18: (AddressMode.IMPLIED, 1, 2, 0)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):  # pylint: disable=unused-argument
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        mcu.sr.C = 0


class CLD(Instruction):  # pylint: disable=too-few-public-methods
    """Clear Decimal Mode"""

    MNEMONIC = 'CLD'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0xD8: (AddressMode.IMPLIED, 1, 2, 0)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):  # pylint: disable=unused-argument
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        mcu.sr.D = 0


class CLI(Instruction):  # pylint: disable=too-few-public-methods
    """Clear Interrupt Disable Bit"""

    MNEMONIC = 'CLI'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0x58: (AddressMode.IMPLIED, 1, 2, 0)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):  # pylint: disable=unused-argument
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        mcu.sr.I = 0


class CLV(Instruction):  # pylint: disable=too-few-public-methods
    """Clear Overflow Flag"""

    MNEMONIC = 'CLV'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0xB8: (AddressMode.IMPLIED, 1, 2, 0)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):  # pylint: disable=unused-argument
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        mcu.sr.V = 0


class CMP(Instruction):  # pylint: disable=too-few-public-methods
    """Compare Memory with Accumulator"""

    MNEMONIC = 'CMP'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0xC9: (AddressMode.IMMEDIATE, 2, 2, 0),
        0xC5: (AddressMode.ZEROPAGE, 2, 3, 0),
        0xD5: (AddressMode.ZEROPAGE_X_INDEXED, 2, 4, 0),
        0xCD: (AddressMode.ABSOLUTE, 3, 4, 0),
        0xDD: (AddressMode.ABSOLUTE_X_INDEXED, 3, 4, 1),
        0xD9: (AddressMode.ABSOLUTE_Y_INDEXED, 3, 4, 1),
        0xC1: (AddressMode.INDEXED_X_INDIRECT, 2, 6, 0),
        0xD1: (AddressMode.INDIRECT_Y_INDEXED, 2, 5, 1)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        mode, _, _, _ = CMP.INSTRUCTIONS[opcode]
        operand, _ = AddressMode.calculate_operand(mode, bytez, mcu, memory)

        val = mcu.a.value - operand
        mcu.sr.set_flags(val, 'NZC')


class CPX(Instruction):  # pylint: disable=too-few-public-methods
    """Compare Memory and Index X"""

    MNEMONIC = 'CPX'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0xE0: (AddressMode.IMMEDIATE, 2, 2, 0),
        0xE4: (AddressMode.ZEROPAGE, 2, 3, 0),
        0xEC: (AddressMode.ABSOLUTE, 3, 4, 0)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        mode, _, _, _ = CPX.INSTRUCTIONS[opcode]
        operand, _ = AddressMode.calculate_operand(mode, bytez, mcu, memory)

        val = mcu.x.value - operand
        mcu.sr.set_flags(val, 'NZC')


class CPY(Instruction):  # pylint: disable=too-few-public-methods
    """Compare Memory and Index Y"""

    MNEMONIC = 'CPY'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0xC0: (AddressMode.IMMEDIATE, 2, 2, 0),
        0xC4: (AddressMode.ZEROPAGE, 2, 3, 0),
        0xCC: (AddressMode.ABSOLUTE, 3, 4, 0)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        mode, _, _, _ = CPY.INSTRUCTIONS[opcode]
        operand, _ = AddressMode.calculate_operand(mode, bytez, mcu, memory)

        val = mcu.y.value - operand
        mcu.sr.set_flags(val, 'NZC')


class DEC(Instruction):  # pylint: disable=too-few-public-methods
    """Decrement Memory by One"""

    MNEMONIC = 'DEC'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0xC6: (AddressMode.ZEROPAGE, 2, 5, 0),
        0xD6: (AddressMode.ZEROPAGE_X_INDEXED, 2, 6, 0),
        0xCE: (AddressMode.ABSOLUTE, 3, 3, 0),
        0xDE: (AddressMode.ABSOLUTE_X_INDEXED, 3, 7, 0)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        mode, _, _, _ = CPY.INSTRUCTIONS[opcode]
        operand, address = AddressMode.calculate_operand(mode, bytez, mcu, memory)

        val = operand - 1
        memory.write_byte(address, val)

        mcu.sr.set_flags(val, 'NZ')


class DEX(Instruction):  # pylint: disable=too-few-public-methods
    """Decrement Index X by One"""

    MNEMONIC = 'DEX'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0xCA: (AddressMode.IMPLIED, 1, 2, 0)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):  # pylint: disable=unused-argument
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """

        val = mcu.x.value - 1
        mcu.x.value = val

        mcu.sr.set_flags(val, 'NZ')


class DEY(Instruction):  # pylint: disable=too-few-public-methods
    """Decrement Index Y by One"""

    MNEMONIC = 'DEY'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0x88: (AddressMode.IMPLIED, 1, 2, 0)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):  # pylint: disable=unused-argument
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """

        val = mcu.x.value - 1
        mcu.y.value = val

        mcu.sr.set_flags(val, 'NZ')


class EOR(Instruction):  # pylint: disable=too-few-public-methods
    """Exclusive-OR Memory with Accumulator"""

    MNEMONIC = 'EOR'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0x49: (AddressMode.IMMEDIATE, 2, 2, 0),
        0x45: (AddressMode.ZEROPAGE, 2, 3, 0),
        0x55: (AddressMode.ZEROPAGE_X_INDEXED, 2, 4, 0),
        0x4D: (AddressMode.ABSOLUTE, 3, 4, 0),
        0x5D: (AddressMode.ABSOLUTE_X_INDEXED, 3, 4, 1),
        0x59: (AddressMode.ABSOLUTE_Y_INDEXED, 3, 4, 1),
        0x41: (AddressMode.INDEXED_X_INDIRECT, 2, 6, 0),
        0x51: (AddressMode.INDIRECT_Y_INDEXED, 2, 5, 1)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        mode, _, _, _ = EOR.INSTRUCTIONS[opcode]
        operand, _ = AddressMode.calculate_operand(mode, bytez, mcu, memory)

        val = mcu.a.value ^ operand
        mcu.a.value = val

        mcu.sr.set_flags(val, 'NZ')


class INC(Instruction):  # pylint: disable=too-few-public-methods
    """Increment Memory by One"""

    MNEMONIC = 'INC'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0xE6: (AddressMode.ZEROPAGE, 2, 5, 0),
        0xF6: (AddressMode.ZEROPAGE_X_INDEXED, 2, 6, 0),
        0xEE: (AddressMode.ABSOLUTE, 3, 6, 0),
        0xFE: (AddressMode.ABSOLUTE_X_INDEXED, 3, 7, 0)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        mode, _, _, _ = INC.INSTRUCTIONS[opcode]
        operand, address = AddressMode.calculate_operand(mode, bytez, mcu, memory)

        val = operand + 1
        memory.write_byte(address, val)

        mcu.sr.set_flags(val, 'NZ')


class INX(Instruction):  # pylint: disable=too-few-public-methods
    """Increment Index X by One"""

    MNEMONIC = 'INX'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0xE8: (AddressMode.IMPLIED, 1, 2, 0)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):  # pylint: disable=unused-argument
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        val = mcu.x.value + 1
        mcu.x.value = val

        mcu.sr.set_flags(val, 'NZ')


class INY(Instruction):  # pylint: disable=too-few-public-methods
    """Increment Index Y by One"""

    MNEMONIC = 'INY'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0xC8: (AddressMode.IMPLIED, 1, 2, 0)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):  # pylint: disable=unused-argument
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        val = mcu.y.value + 1
        mcu.y.value = val

        mcu.sr.set_flags(val, 'NZ')


class JMP(Instruction):  # pylint: disable=too-few-public-methods
    """Jump to New Location"""

    MNEMONIC = 'JMP'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0x4C: (AddressMode.ABSOLUTE, 3, 3, 0),
        0x6C: (AddressMode.INDIRECT, 3, 5, 0)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        mode, _, _, _ = JMP.INSTRUCTIONS[opcode]
        operand, _ = AddressMode.calculate_operand(mode, bytez, mcu, memory)

        mcu.pc.value = operand


class JSR(Instruction):  # pylint: disable=too-few-public-methods
    """Jump to New Location Saving Return Address"""

    MNEMONIC = 'JSR'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0x20: (AddressMode.ABSOLUTE, 3, 6, 0)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        mode, _, _, _ = JMP.INSTRUCTIONS[opcode]
        operand, _ = AddressMode.calculate_operand(mode, bytez, mcu, memory)

        memory.write_word(mcu.sp.value, mcu.pc + 2)
        mcu.sp.value = mcu.sp.value - 2

        mcu.pc.value = operand


class LDA(Instruction):  # pylint: disable=too-few-public-methods
    """Load Accumulator with Memory"""

    MNEMONIC = 'LDA'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0xA9: (AddressMode.IMMEDIATE, 2, 2, 0),
        0xA5: (AddressMode.ZEROPAGE, 2, 3, 0),
        0xB5: (AddressMode.ZEROPAGE_X_INDEXED, 2, 4, 0),
        0xAD: (AddressMode.ABSOLUTE, 3, 4, 0),
        0xBD: (AddressMode.ABSOLUTE_X_INDEXED, 3, 4, 1),
        0xB9: (AddressMode.ABSOLUTE_Y_INDEXED, 3, 4, 1),
        0xA1: (AddressMode.INDEXED_X_INDIRECT, 2, 6, 0),
        0xB1: (AddressMode.INDIRECT_Y_INDEXED, 2, 5, 1)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        mode, _, _, _ = LDA.INSTRUCTIONS[opcode]
        operand, _ = AddressMode.calculate_operand(mode, bytez, mcu, memory)

        mcu.a.value = operand

        mcu.sr.set_flags(operand, 'NZ')


class LDX(Instruction):  # pylint: disable=too-few-public-methods
    """Load Index X with Memory"""

    MNEMONIC = 'LDX'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0xA2: (AddressMode.IMMEDIATE, 2, 2, 0),
        0xA6: (AddressMode.ZEROPAGE, 2, 3, 0),
        0xB6: (AddressMode.ZEROPAGE_Y_INDEXED, 2, 4, 0),
        0xAE: (AddressMode.ABSOLUTE, 3, 4, 0),
        0xBE: (AddressMode.ABSOLUTE_Y_INDEXED, 3, 4, 1)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        mode, _, _, _ = LDX.INSTRUCTIONS[opcode]
        operand, _ = AddressMode.calculate_operand(mode, bytez, mcu, memory)

        mcu.x.value = operand

        mcu.sr.set_flags(operand, 'NZ')


class LDY(Instruction):  # pylint: disable=too-few-public-methods
    """Load Index Y with Memory"""

    MNEMONIC = 'LDY'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0xA0: (AddressMode.IMMEDIATE, 2, 2, 0),
        0xA4: (AddressMode.ZEROPAGE, 2, 3, 0),
        0xB4: (AddressMode.ZEROPAGE_Y_INDEXED, 2, 4, 0),
        0xAC: (AddressMode.ABSOLUTE, 3, 4, 0),
        0xBC: (AddressMode.ABSOLUTE_Y_INDEXED, 3, 4, 1)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        mode, _, _, _ = LDY.INSTRUCTIONS[opcode]
        operand, _ = AddressMode.calculate_operand(mode, bytez, mcu, memory)

        mcu.y.value = operand

        mcu.sr.set_flags(operand, 'NZ')


class LSR(Instruction):  # pylint: disable=too-few-public-methods
    """Shift One Bit Right (Memory or Accumulator)"""
    # TODO: Implement
    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        pass


class NOP(Instruction):  # pylint: disable=too-few-public-methods
    """No Operation"""

    MNEMONIC = 'NOP'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0xEA: (AddressMode.IMPLIED, 1, 2, 0)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        pass


class ORA(Instruction):  # pylint: disable=too-few-public-methods
    """OR Memory with Accumulator"""

    MNEMONIC = 'ORA'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0x09: (AddressMode.IMMEDIATE, 2, 2, 0),
        0x05: (AddressMode.ZEROPAGE, 2, 3, 0),
        0x15: (AddressMode.ZEROPAGE_X_INDEXED, 2, 4, 0),
        0x0D: (AddressMode.ABSOLUTE, 3, 4, 0),
        0x1D: (AddressMode.ABSOLUTE_X_INDEXED, 3, 4, 1),
        0x19: (AddressMode.ABSOLUTE_Y_INDEXED, 3, 4, 1),
        0x01: (AddressMode.INDEXED_X_INDIRECT, 2, 6, 0),
        0x11: (AddressMode.INDIRECT_Y_INDEXED, 2, 5, 1)
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        mode, _, _, _ = ORA.INSTRUCTIONS[opcode]
        operand, _ = AddressMode.calculate_operand(mode, bytez, mcu, memory)

        val = mcu.a.value | operand
        mcu.a.value = val

        mcu.sr.set_flags(val, 'NZ')


class PHA(Instruction):  # pylint: disable=too-few-public-methods
    """Push Accumulator on Stack"""

    MNEMONIC = 'PHY'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0x48: (AddressMode.IMPLIED, 1, 3, 0),
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):  # pylint: disable=unused-argument
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        memory.write_byte(mcu.sp.value, mcu.a.value)
        mcu.sp.value = mcu.sp.value - 1


class PHP(Instruction):  # pylint: disable=too-few-public-methods
    """Push Processor Status on Stack"""

    MNEMONIC = 'PHP'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0x08: (AddressMode.IMPLIED, 1, 3, 0),
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):  # pylint: disable=unused-argument
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        memory.write_byte(mcu.sp.value, mcu.sr.value)
        mcu.sp.value = mcu.sp.value - 1


class PLA(Instruction):  # pylint: disable=too-few-public-methods
    """Pull Accumulator from Stack"""

    MNEMONIC = 'PLA'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0x68: (AddressMode.IMPLIED, 1, 4, 0),
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):  # pylint: disable=unused-argument
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        mcu.a.value = memory.read_byte(mcu.sp.value)
        mcu.sp.value = mcu.sp.value + 1


class PLP(Instruction):  # pylint: disable=too-few-public-methods
    """Pull Processor Status from Stack"""

    MNEMONIC = 'PLP'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0x28: (AddressMode.IMPLIED, 1, 4, 0),
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):  # pylint: disable=unused-argument
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        mcu.sr.value = memory.read_byte(mcu.sp.value)
        mcu.sp.value = mcu.sp.value + 1


class ROL(Instruction):  # pylint: disable=too-few-public-methods
    """Rotate One Bit Left (Memory or Accumulator)"""
    # TODO: Implement
    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        pass


class ROR(Instruction):  # pylint: disable=too-few-public-methods
    """Rotate One Bit Right (Memory or Accumulator)"""
    # TODO: Implements
    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        pass


class RTI(Instruction):  # pylint: disable=too-few-public-methods
    """Return from Interrupt"""

    MNEMONIC = 'RTI'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0x40: (AddressMode.IMPLIED, 1, 6, 0),
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):  # pylint: disable=unused-argument
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        mcu.sr.value = memory.read_byte(mcu.sp.value)
        mcu.sp.value = mcu.sp.value + 1

        mcu.pc.value = memory.read_byte(mcu.sp.value)
        mcu.sp.value = mcu.sp.value + 1


class RTS(Instruction):  # pylint: disable=too-few-public-methods
    """Return from Subroutine"""

    MNEMONIC = 'RTS'
    # Dict of tuples (#address_mode, #bytes, #cycles, #page_boundary_cycles) keyed by #opcode
    INSTRUCTIONS = {
        0x60: (AddressMode.IMPLIED, 1, 6, 0),
    }

    @staticmethod
    def execute(opcode, bytez, mcu, memory):  # pylint: disable=unused-argument
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        val = memory.read_byte(mcu.sp.value)
        mcu.sp.value = mcu.sp.value + 1

        mcu.pc.value = val + 1


class SBC(Instruction):  # pylint: disable=too-few-public-methods
    """Subtract Memory from Accumulator with Borrow"""

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        pass


class SEC(Instruction):  # pylint: disable=too-few-public-methods
    """Set Carry Flag"""

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        pass


class SED(Instruction):  # pylint: disable=too-few-public-methods
    """Set Decimal Flag"""

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        pass


class SEI(Instruction):  # pylint: disable=too-few-public-methods
    """Set Interrupt Disable Status"""

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        pass


class STA(Instruction):  # pylint: disable=too-few-public-methods
    """Store Accumulator in Memory"""

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        pass


class STX(Instruction):  # pylint: disable=too-few-public-methods
    """Store Index X in Memory"""

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        pass


class STY(Instruction):  # pylint: disable=too-few-public-methods
    """Sore Index Y in Memory"""

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        pass


class TAX(Instruction):  # pylint: disable=too-few-public-methods
    """Transfer Accumulator to Index X"""

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        pass


class TAY(Instruction):  # pylint: disable=too-few-public-methods
    """Transfer Accumulator to Index Y"""

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        pass


class TSX(Instruction):  # pylint: disable=too-few-public-methods
    """Transfer Stack Pointer to Index X"""

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        pass


class TXA(Instruction):  # pylint: disable=too-few-public-methods
    """Transfer Index X to Accumulator"""

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        pass


class TXS(Instruction):  # pylint: disable=too-few-public-methods
    """Transfer Index X to Stack Register"""

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        pass


class TYA(Instruction):  # pylint: disable=too-few-public-methods
    """Transfer Index Y to Accumulator"""

    @staticmethod
    def execute(opcode, bytez, mcu, memory):
        """
        Execute command.

        :param opcode: Command opcode.
        :param bytez: Command bytes.
        :param mcu: MCU instance.
        :param memory: Memory instance.
        :return: Nothing.
        """
        pass


if __name__ == '__main__':
    pass