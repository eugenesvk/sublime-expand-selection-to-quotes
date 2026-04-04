import sublime, sublime_plugin

class ExpandSelectionToQuotesCommand(sublime_plugin.TextCommand):
	q_same = ('"', "'", "`")
	esc    = "\\"

	def run(self, edit):
		q_all = {}
		for q in self.q_same:
			q_all[q] = list(map(lambda x: x.begin(), self.view.find_all(q)))

		def search_for_quotes(q_type, quotes):
			q_size, before, after = False, False, False

			if len(quotes) - self.view.substr(sel).count('"') >= 2:
				all_before = list(filter(lambda x: x <  sel.begin(), quotes))
				all_after  = list(filter(lambda x: x >= sel.end  (), quotes))
				before, after = None, None

				if all_before: # Find escaped quotes and skip them
					for  i_q in reversed(all_before):
						if i_q == 0:
							before = i_q
							break
						else:
							char_pre_q = self.view.substr(i_q - 1)
							if not char_pre_q == self.esc:
								before = i_q
								break
				if all_after:
					for  i_q in          all_after  :
						if i_q == 0: # shouldn't happen, but just in case
							after = i_q
							break
						else:
							char_pre_q = self.view.substr(i_q - 1)
							if not char_pre_q == self.esc:
								after = i_q
								break

				if before is not None and after is not None: q_size = after - before

			return q_size, before, after

		def replace_region(start, end):
			if sel.size() < end-start-2:
				start += 1; end -= 1
			self.view.sel().subtract(sel)
			self.view.sel().add(sublime.Region(start, end))

		for sel in self.view.sel():
			q_res = {}
			for q in self.q_same:
				sz, pre, pos = search_for_quotes(q,q_all[q])
				q_res[sz] = (pre,pos)

			min_sz = None
			for sz in q_res: # find the nearest quotes…
				if sz:
					if not min_sz:
						min_sz =     sz
					else:
						min_sz = min(sz, min_sz)
			if min_sz:      # …use their region for selection
				replace_region(q_res[min_sz][0], q_res[min_sz][1] + 1)
