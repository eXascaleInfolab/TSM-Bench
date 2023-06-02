package cn.edu.fudan.cs.dstree.util.system;

import java.util.List;

public interface RuntimeInformation {
    long getTotalHeapMemory();

    long getTotalHeapMemoryUsed();

    String getJvmInputArguments();

    /**
     * Get information about all the specific memory pools currently in use.
     *
     * @return
     */
    List<MemoryInformation> getMemoryPoolInformation();

    /**
     * Total PermGen if PermGen used on this VM
     *
     * @return the total amount of perm gen allocated if perm gen is supported on this VM or -1 if not
     */
    long getTotalPermGenMemory();

    /**
     * Used PermGen if PermGen used on this VM
     *
     * @return the used amount of perm gen if perm gen is supported on this VM or -1 if not
     */
    long getTotalPermGenMemoryUsed();

    /**
     * Total non heap if non heap is used on this VM
     *
     * @return the total amount of non heap allocated if supported on this VM or -1 if not
     */
    long getTotalNonHeapMemory();

    /**
     * Used non heap if non heap is used on this VM
     *
     * @return the used amount of non heap allocated if supported on this VM or -1 if not
     */
    long getTotalNonHeapMemoryUsed();
}