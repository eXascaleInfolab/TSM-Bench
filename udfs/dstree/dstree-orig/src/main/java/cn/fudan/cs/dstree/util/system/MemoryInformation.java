package cn.edu.fudan.cs.dstree.util.system;

/**
 * MemoryInformation stores information about a specific memory pool such as eden, old or permgen.
 * Different JVMs have different memory map implementations.
 */
public interface MemoryInformation {
    String getName();

    long getTotal();

    long getUsed();

    long getFree();
}
