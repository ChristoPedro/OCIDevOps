using System.Threading;
using System.Threading.Tasks;
using FnProject.Fdk;

namespace csharpfn
{
	public class Function
	{
		public Task<string> InvokeAsync(string input, CancellationToken timedOut)
		{
			if (string.IsNullOrWhiteSpace(input))
			{
				input = "world";
			}
			return Task.FromResult("Hello " + input);
		}

		public static void Main()
		{
			FdkHandler.Handle<Function>();
		}
	}
}
