function confirmDelete() {
        if (confirm("Are you sure you want to delete this data?")) {
            // If the user clicks "OK" on the confirmation box, delete the data using an AJAX call.
            $.ajax({
                type: "POST",
                url: "{{ url_for('delete_data') }}",
                success: function() {
                    // If the deletion is successful, redirect the user to a success page or refresh the current page.
                    alert("Deleted!")
                },
                error: function() {
                    // If there is an error with the deletion, show an error message.
                    alert("There was an error deleting the data.");
                }
            });
        }
    }