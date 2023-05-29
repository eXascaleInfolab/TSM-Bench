package cn.edu.fudan.cs.dstree.util.system;

import java.util.List;

public interface SystemInfoUtils {
    public static final long MEGABYTE = 0x100000L;

    public abstract long getTotalMemory();

    public abstract long getFreeMemory();

    public abstract long getUsedMemory();

    public abstract List getMemoryPoolInformation();

    public abstract long getTotalPermGenMemory();

    public abstract long getFreePermGenMemory();

    public abstract long getUsedPermGenMemory();

    public abstract long getTotalNonHeapMemory();

    public abstract long getFreeNonHeapMemory();

    public abstract long getUsedNonHeapMemory();

    public abstract String getJvmInputArguments();
}
