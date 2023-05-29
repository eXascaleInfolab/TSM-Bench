package cn.edu.fudan.cs.dstree.util.system;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

public class SystemInfoUtilsImpl implements SystemInfoUtils {
    private final Runtime rt = Runtime.getRuntime();
    private final RuntimeInformation runtimeInformation = RuntimeInformationFactory.getRuntimeInformation();

    public SystemInfoUtilsImpl() {
    }

    public long getTotalMemory() {
        long totalMemory = rt.maxMemory();
        return totalMemory / 0x100000L;
    }

    public long getFreeMemory() {
        long freeMemory = (rt.maxMemory() - rt.totalMemory()) + rt.freeMemory();
        return freeMemory / 0x100000L;
    }

    public long getUsedMemory() {
        return getTotalMemory() - getFreeMemory();
    }

    public List getMemoryPoolInformation() {
        List list = runtimeInformation.getMemoryPoolInformation();
        List validList = new ArrayList();
        for (Iterator i$ = list.iterator(); i$.hasNext(); ) {
            MemoryInformation memoryInfo = (MemoryInformation) i$.next();
            try {
                memoryInfo.toString();
                validList.add(memoryInfo);
            } catch (RuntimeException e) {
            }
        }

        return validList;
    }

    public long getTotalPermGenMemory() {
        return runtimeInformation.getTotalPermGenMemory() / 0x100000L;
    }

    public long getFreePermGenMemory() {
        long freeMemory = runtimeInformation.getTotalPermGenMemory() - runtimeInformation.getTotalPermGenMemoryUsed();
        return freeMemory / 0x100000L;
    }

    public long getUsedPermGenMemory() {
        return runtimeInformation.getTotalPermGenMemoryUsed() / 0x100000L;
    }

    public long getTotalNonHeapMemory() {
        return runtimeInformation.getTotalNonHeapMemory() / 0x100000L;
    }

    public long getFreeNonHeapMemory() {
        long freeMemory = runtimeInformation.getTotalNonHeapMemory() - runtimeInformation.getTotalNonHeapMemoryUsed();
        return freeMemory / 0x100000L;
    }

    public long getUsedNonHeapMemory() {
        return runtimeInformation.getTotalNonHeapMemoryUsed() / 0x100000L;
    }

    public String getJvmInputArguments() {
        return runtimeInformation.getJvmInputArguments();
    }
}
