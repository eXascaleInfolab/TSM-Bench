package cn.edu.fudan.cs.dstree.util.system;

import java.util.List;

import static java.util.Collections.emptyList;

public class RuntimeInformationStub implements RuntimeInformation {
    public String getJvmInputArguments() {
        return "Unknown";
    }

    public long getTotalHeapMemory() {
        return 0;
    }

    public long getTotalHeapMemoryUsed() {
        return 0;
    }

    public List<MemoryInformation> getMemoryPoolInformation() {
        return emptyList();
    }

    public long getTotalPermGenMemory() {
        return 0;
    }

    public long getTotalPermGenMemoryUsed() {
        return 0;
    }

    public long getTotalNonHeapMemory() {
        return 0;
    }

    public long getTotalNonHeapMemoryUsed() {
        return 0;
    }
}