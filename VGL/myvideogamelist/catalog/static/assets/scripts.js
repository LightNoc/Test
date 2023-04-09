function quicksort(arr, left, right, column) {
    var pivot, partitionIndex;

    if (left < right) {
        pivot = right;
        partitionIndex = partition(arr, pivot, left, right, column);

        quicksort(arr, left, partitionIndex - 1, column);
        quicksort(arr, partitionIndex + 1, right, column);
    }
    return arr;
}

function partition(arr, pivot, left, right, column) {
    var pivotValue = arr[pivot][column],
        partitionIndex = left;

    for (var i = left; i < right; i++) {
        if (arr[i][column] < pivotValue) {
            swap(arr, i, partitionIndex);
            partitionIndex++;
        }
    }
    swap(arr, right, partitionIndex);
    return partitionIndex;
}

function swap(arr, i, j) {
    var temp = arr[i];
    arr[i] = arr[j];
    arr[j] = temp;
}
function sortTable(n) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById("games-table");
    switching = true;
    dir = "asc";
    while (switching) {
        switching = false;
        rows = table.rows;
        var games = [];
        for (i = 1; i < (rows.length - 1); i++) {
            games.push(rows[i]);
        }
        games = quicksort(games, 0, games.length - 1, n);
        for (i = 0; i < games.length; i++) {
            table.appendChild(games[i]);
        }
    }
}